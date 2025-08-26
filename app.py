__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import spacy
from sentence_transformers import SentenceTransformer
import chromadb
from transformers import pipeline
import json
from huggingface_hub import InferenceClient
from openai import OpenAI
import streamlit as st
import mysql.connector
from mysql.connector import Error

# Load key from streamlit secrets
openai_api_key = st.secrets["openAI_key"]
OpenAIClient = OpenAI(api_key=openai_api_key)  # Replace with your OpenAI API key
dbhost = st.secrets["host"]
dbport = st.secrets["port"]
dbuser = st.secrets["user"]
dbpassword = st.secrets["password"]
dbdatabase = st.secrets["database"]

# Load models
@st.cache_resource
def load_symptoms_model():
    return spacy.load("symptom_ner_model")

@st.cache_resource
def load_embedder_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource  # if using Streamlit
def get_chroma_client():
    return chromadb.PersistentClient(path="./chromadb_store")


# Load models
nlp = load_symptoms_model()
embedder = load_embedder_model()

# ChromaDB client
client = get_chroma_client()
collection = client.get_or_create_collection(name="ayurveda_symptoms")

# FastAPI app
app = FastAPI(title="Ayurveda Remedy API")

# Allow Streamlit to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def _as_string(obj):
        if obj is None:
            return ""
        if isinstance(obj, str):
            return obj
        if isinstance(obj, dict):
            return json.dumps(obj, ensure_ascii=False)
        if isinstance(obj, list):
            # if all items are strings, join them, otherwise serialize as JSON
            if all(isinstance(x, str) for x in obj):
                return ", ".join(obj)
            try:
                return json.dumps(obj, ensure_ascii=False)
            except TypeError:
                return ", ".join(map(str, obj))
        return str(obj)

def insert_interactions(user_query, extracted_symptoms, system_response, score, openAI_response):
    """
    Inserts one or more interaction records into the MySQL `interactions` table.
    
    :param records: List of tuples, each tuple matches the
                    (user_query, extracted_symptoms, system_response, score, openAI_response)
    """
    records = [(_as_string(user_query), 
                _as_string(extracted_symptoms), 
                _as_string(system_response), 
                float(score) if score is not None else 0.0, 
                _as_string(openAI_response))]
    try:
        # 1. Establish a connection
        conn = mysql.connector.connect(
            host=dbhost
            port=dbport,                # default MySQL port
            user=dbuser,
            password=dbpassword,
            database=dbdatabase
        )
        if not conn.is_connected():
            raise Error("Failed to connect to database")

        cursor = conn.cursor()

        # 2. Prepare the INSERT statement
        sql = """
            INSERT INTO interactions
                (user_query, extracted_symptoms, system_response, score, openAI_response)
            VALUES
                (%s, %s, %s, %s, %s)
        """

        # 3. Execute one or multiple inserts
        cursor.executemany(sql, records)

        # 4. Commit to persist changes
        conn.commit()
        print(f"{cursor.rowcount} record(s) inserted, last insert ID: {cursor.lastrowid}")

    except Error as e:
        print("Error:", e)
    finally:
        # 5. Clean up
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

class QueryRequest(BaseModel):
    query: str

@app.post("/get_remedy")
def get_remedy(request: QueryRequest):
    user_input = request.query   
    doc = nlp(user_input)
    extracted_symptoms = [ent.text for ent in doc.ents if ent.label_ == "SYMPTOM"]
    print("Extracted Symptoms:", extracted_symptoms)

    if not extracted_symptoms:
        print("No symptoms detected.")
        return {"recommendation": "I'm sorry, I couldn't identify any symptoms in your input. Please provide more details about your symptoms."}
    else:
        # Step 3: Embed extracted symptoms
        query_embedding = embedder.encode(", ".join(extracted_symptoms)).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        matches = []
        calcscore = 0
        for i, doc in enumerate(results['documents'][0]):
            score = results['distances'][0][i]
            similarity = 1 - score
            print(f"\nMatch #{i+1}")
            print("Score (distance):", score)
            print("Similarity:", similarity)
            print("Matched Symptoms:", doc)
            print("Disease:", results['metadatas'][0][i]['disease'])
            print("Dosha:", results['metadatas'][0][i]['dosha'])
            print("Remedies:", json.dumps(results['metadatas'][0][i]['remedy'], indent=2))
            calcscore += score
            matches.append({
                "symptoms": doc,
                "disease": results['metadatas'][0][i]['disease'],
                "dosha": results['metadatas'][0][i]['dosha'],
                "remedy": json.dumps(results['metadatas'][0][i]['remedy'], indent=2),
                "similarity": similarity
            })
        avgscore = calcscore / len(matches)
        print("Average Score (distance):", avgscore)

        context_text = "\n\n".join([
        f"Match {i+1} (Similarity: {m['similarity']:.2f}):\n"
        f"Symptoms: {m['symptoms']}\n"
        f"Disease: {m['disease']}\n"
        f"Dosha: {m['dosha']}\n"
        f"Remedy: {json.dumps(m['remedy'], indent=2)}"
        for i, m in enumerate(matches)
            ])

        prompt = f"""
        You are an Ayurvedic assistant. The patient reports: {user_input}.
        We have the following top 3 matches from our database:

        {context_text}

        Based on this information, choose the most relevant match and explain it to the user clearly. 
        Include the disease name, dosha, and remedies in natural language.
        """
        
        response = OpenAIClient.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are an expert Ayurveda medical assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        #response = "The best match is Match 1: Acne \u2014 a Pitta-type condition. Pitta imbalance in the skin produces heat and inflammation, so acne often appears as red, inflamed pimples that can flare with emotional stress, premenstrual or hormonal changes, too much sun, chemical exposure, or bacterial irritation.\n\nRecommended Ayurvedic approach (what to do):\n\n1. Internal/herbal remedies\n- Cumin\u2013coriander\u2013fennel tea: 1/3 teaspoon each, steep and drink after meals, three times daily \u2014 cooling and digestion-supporting. \n- Kutki + guduchi + shatavari: about 1/4 teaspoon (combined) after meals, 2\u20133 times/day \u2014 helps reduce internal heat and supports liver/immune balance. \n- Amalaki powder (Indian gooseberry): 1/2\u20131 teaspoon before bed \u2014 cooling and antioxidant. \n- Aloe vera juice: 1/2 cup twice daily \u2014 soothes and cools Pitta.\n\n2. Topical, external care\n- Almond paste: apply on affected areas and leave for ~30 minutes, then rinse \u2014 gentle nourishment. \n- Sandalwood + turmeric paste mixed with goat\u2019s milk: cooling, anti-inflammatory paste for spot application. \n- Chickpea (gram) flour paste: gentle cleanser/mask to absorb oil and calm skin. \n- Rubbing melon on the skin overnight or using fresh cooling pulp can soothe inflamed spots.\n\n3. Diet and daily regimen (pathya)\n- Follow a Pitta\u2011pacifying diet: favor bland, cooling foods \u2014 rice, oatmeal, applesauce. \n- Avoid spicy, fried, fermented, very salty foods and citrus fruits, and reduce alcohol and caffeine. \n- Limit direct sun exposure and avoid chemical irritants on skin (harsh cosmetics).\n\n4. Lifestyle, stress and breathing\n- Manage stress with visualization/meditation. \n- Practice left\u2011nostril breathing (Chandra/soft-moon breath) 5\u201310 minutes daily to calm Pitta. \n- Gentle yoga: Moon salutation and Lion pose can be helpful. \n- Reduce behaviors that increase emotional strain (for example, avoid frequent mirror\u2011checking).\n\n5. Miscellaneous\n- Keep the face clean with gentle, non\u2011irritating products. Avoid harsh scrubs or frequent picking. \n- If there are signs of a bacterial infection (increasing pain, warmth, spreading redness, fever) or severe/nodular acne, see a dermatologist for evaluation and possible medical treatment.\n\nIf you\u2019d like, I can turn this into a simple daily plan (what to take/when and a short morning/evening routine) based on your current medications and any allergies."
        print("Response from OpenAI:", response.choices[0].message.content)
        insert_interactions(user_input, extracted_symptoms, matches, avgscore, response.choices[0].message.content)
        
        return {
        "extracted_symptoms": extracted_symptoms,
        "matches": matches,
        "recommendation": response.choices[0].message.content
        }

#--------------UI Code from ui.py------------------
import streamlit as st
import requests
import re

#API_URL = "http://localhost:8000/get_remedy"
API_URL = "http://127.0.0.1:8000/get_remedy"

st.set_page_config(page_title="Ayurveda Remedy Chatbot", page_icon="🌿",layout="centered")
st.title("🪷 Ayurveda Remedy Recommender")

def clean_llm_response(response: str):
    """
    Cleans LLM response by removing generic or unnecessary text.
    """
    # Remove unwanted generic suggestions
    response = re.sub(r"If you’d like.*", "", response, flags=re.DOTALL)
    return response.strip()

def format_llm_response(response_text: str):
    raw_text = clean_llm_response(response_text)
    # Normalize unicode and line breaks
    text = raw_text.encode().decode("unicode_escape")
    text = text.replace("\\n", "\n").replace("\u2014", "—")

    # Split into sections based on numbers or keywords
    sections = re.split(r"\n(?=\d+\.)", text)

    st.subheader("🤖 Bot Response")

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # First part (before the numbered list)
        if not re.match(r"^\d+\.", section):
            st.markdown(f"**{section}**")
            continue

        # Numbered sections
        lines = section.split("\n")
        header = lines[0]  # like "1. Internal/herbal remedies"
        content = lines[1:]

        with st.expander(header):
            for line in content:
                line = line.strip()
                if line.startswith("-"):
                    st.write(f"• {line[1:].strip()}")
                elif line:
                    st.write(line)


if "messages" not in st.session_state:
    st.session_state.messages = []

def stream_generator():
    for word in data["recommendation"].split():
        yield word + " "

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**🧑 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 Bot:** {msg['content']}")

# User input
user_input = st.text_input("Enter your symptoms:", key="user_input")

if st.button("Get Remedy"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Finding remedy..."):
            #res = requests.post(API_URL, json={"query": user_input})
            res = get_remedy(QueryRequest(query=user_input))

        data = res
        if "recommendation" in data:
            #formatted_output = format_llm_response(data["recommendation"])
            st.write_stream(stream_generator())                
            #bot_reply = formatted_output            
                
        elif "matches" in data:
            matches = data["matches"]
            if matches:
                bot_reply = "Here are the top matches for your symptoms:\n\n"
                for match in matches:
                    bot_reply += f"- **Disease:** {match['disease']}\n"
                    bot_reply += f"  **Dosha:** {match['dosha']}\n"
                    bot_reply += f"  **Remedies:** {match['remedy']}\n\n"
            else:
                bot_reply = "No matching remedies found for your symptoms."
        else:
            bot_reply = "No remedy found for given symptoms."

        st.session_state.messages.append({"role": "bot", "content": data["recommendation"]})
        
    st.rerun()














