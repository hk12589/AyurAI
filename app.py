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
            host=dbhost,
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
import app as app
from app import get_remedy, QueryRequest

#API_URL = "http://localhost:8000/get_remedy"
API_URL = "http://127.0.0.1:8000/get_remedy"

st.set_page_config(page_title="Ayurveda Remedy Chatbot", page_icon="🌿",layout="wide")
st.title("🪷 Ayurveda Remedy Recommender")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("How can I help you?", key="user_prompt"):
    print(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner("Finding remedy..."):            
        response = get_remedy(QueryRequest(query=prompt))
    msg = response["recommendation"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


















