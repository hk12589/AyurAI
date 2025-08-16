import json
import spacy
import nltk
import chromadb
import uuid

from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer

nltk.download("punkt")

# Load NLP models
nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight and fast

# Load dataset
with open("cleaned_ayurveda_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
#data = cleaned_data

# Helper: Flatten symptom or remedy fields
def flatten_text(item):
    flat = []
    if isinstance(item, dict):
        for val in item.values():
            flat.extend(flatten_text(val))
    elif isinstance(item, list):
        for sub in item:
            flat.extend(flatten_text(sub))
    elif isinstance(item, str):
        flat.append(item)
    return flat

# NLP Pipeline
def process_ayurveda_data(data):
    records = []

    for entry in data:
        disease = entry.get("disease", "Unknown")
        dosha = entry.get("primary_dosha", [])

        # --- Symptoms ---
        symptoms = entry.get("symptoms", [])
        symptom_sentences = sent_tokenize(" ".join(symptoms))
        symptom_embeddings = embedder.encode(symptom_sentences)

        # --- Remedies ---
        remedies = entry.get("remedies", {})
        remedy_sentences = sent_tokenize(" ".join(remedies))
        remedy_embeddings = embedder.encode(remedy_sentences)


        records.append({
            "Disease": disease,
            "Dosha": dosha,
            "Symptoms": symptom_sentences,
            "Symptom Embeddings": symptom_embeddings,
            "Remedies": remedy_sentences,
            "Remedy Embeddings": remedy_embeddings,
        })

    return records

results = process_ayurveda_data(data)

# Preview Output
for r in results[:5]:
    print("Disease:", r["Disease"])
    print("Dosha:", r["Dosha"])
    print("Symptoms:", r["Symptoms"][:3])  # Preview first 3
    print("Remedies:", r["Remedies"][:3])

client     = chromadb.PersistentClient(path="./chromadb_store")
collection = client.get_or_create_collection(name="ayurveda_symptoms")

for rec_idx, entry in enumerate(results):
    disease  = entry["Disease"]
    dosha    = ", ".join(entry["Dosha"]) # Convert list of doshas to string
    remedies = entry["Remedies"]

    # 3. For each symptom sentence + its embedding
    for sym_idx, (sym_text, sym_emb) in enumerate(zip(entry["Symptoms"], entry["Symptom Embeddings"])):
        # pick the matching remedy sentence (or join all if uneven lengths)
         remedy_meta = remedies[sym_idx] if sym_idx < len(remedies) else " | ".join(remedies)
         metadata = {
            "disease": disease,
            "dosha": dosha,
            "remedy": remedy_meta
        }
         collection.add(
            ids       = [f"{rec_idx}-{sym_idx}"],      # unique ID per symptom
            embeddings= [sym_emb.tolist()],             # convert numpy array to list
            metadatas = [metadata],
            documents = [sym_text]
        )