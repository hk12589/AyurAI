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
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Load models
nlp = spacy.load("symptom_ner_model")  # Your trained NER model
embedder = SentenceTransformer("all-MiniLM-L6-v2")
OpenAIClient = OpenAI(api_key="openai_api_key")  # Replace with your OpenAI API key


# ChromaDB client
client = chromadb.PersistentClient(path="./chromadb_store")
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

import sqlite3

# Initialize and create table
def init_db():
    conn = sqlite3.connect("ayurAI_chatbot.db")  # this will create DB file if it doesn't exist
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_query TEXT,
        extracted_symptoms TEXT,
        system_response TEXT,
        score REAL,
        openAI_response TEXT,                      
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# Call this once before using DB
init_db()
print("✅ Database initialized and table created successfully.")

# ...start save ingteraction to DB...
def save_interaction(user_query, extracted_symptoms, system_response, score, openAI_response):
    import json
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

    conn = sqlite3.connect("ayurAI_chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interactions (user_query, extracted_symptoms, system_response, score, openAI_response)
        VALUES (?, ?, ?, ?, ?)
    """, (
        _as_string(user_query),
        _as_string(extracted_symptoms),
        _as_string(system_response),
        float(score) if score is not None else None,
        _as_string(openAI_response)
    ))
    conn.commit()
    conn.close()
# ...end save ingteraction to DB...

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
        save_interaction(user_input, extracted_symptoms, matches, avgscore, response.choices[0].message.content)
        
        return {
        "extracted_symptoms": extracted_symptoms,
        "matches": matches,
        "recommendation": response.choices[0].message.content
        }
        

