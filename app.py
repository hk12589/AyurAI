from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import spacy
from sentence_transformers import SentenceTransformer
import chromadb
from transformers import pipeline
import json
from huggingface_hub import InferenceClient

# Load models
nlp = spacy.load("symptom_ner_model")  # Your trained NER model
embedder = SentenceTransformer("all-MiniLM-L6-v2")
qa_model = pipeline("text2text-generation", model="google/flan-t5-large")

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

# Hugging Face API Client
hf_client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.2",
    token="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"
)

# ---------- Helper Functions ----------
def get_best_remedy_from_hf(extracted_symptoms, results):
    # Prepare matches context
    context_parts = []
    for i, doc in enumerate(results['documents'][0]):
        disease = results['metadatas'][0][i]['disease']
        dosha = results['metadatas'][0][i]['dosha']
        remedies = json.dumps(results['metadatas'][0][i]['remedy'], indent=2)
        score = results['distances'][0][i] if 'distances' in results else None
        context_parts.append(
            f"Match #{i+1}\nDisease: {disease}\nDosha: {dosha}\nScore: {score}\nRemedies: {remedies}"
        )

    context_text = "\n\n".join(context_parts)

    # Create prompt for HF model
    user_query = f"""
    The user has the following symptoms: {', '.join(extracted_symptoms)}.
    Based on the matches below, choose the single most relevant disease and provide a clear, concise, human-friendly remedy.

    Matches:
    {context_text}

    Respond only with the final recommended remedy and short instructions.
    """

    # Call Hugging Face API
    response = hf_client.text_generation(
        prompt=user_query,
        max_new_tokens=300,
        temperature=0.3
    )

    return response.strip()

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
    
    for i, doc in enumerate(results['documents'][0]):
        score = results['distances'][0][i]
        similarity = 1 - score
        print(f"\nMatch #{i+1}")
        print("Score (distance):", score)
        print("Matched Symptoms:", doc)
        print("Disease:", results['metadatas'][0][i]['disease'])
        print("Dosha:", results['metadatas'][0][i]['dosha'])
        print("Remedies:", json.dumps(results['metadatas'][0][i]['remedy'], indent=2))
        
        matches.append({
            "symptoms": doc,
            "disease": results['metadatas'][0][i]['disease'],
            "dosha": results['metadatas'][0][i]['dosha'],
            "remedy": json.dumps(results['metadatas'][0][i]['remedy'], indent=2),
            "similarity": similarity
        })

    return {
    "extracted_symptoms": extracted_symptoms,
    "matches": matches,
    "recommendation": json.dumps(matches[0], indent=2)
}
