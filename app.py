from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import json
import os
import traceback
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for models
nlp = None
embedder = None
collection = None

def load_models():
    """Load the AI models and vector database"""
    global nlp, embedder, collection
    
    try:
        # Load spaCy NER model (if it exists)
        if os.path.exists("symptom_ner_model"):
            nlp = spacy.load("symptom_ner_model")
            logger.info("Loaded custom NER model")
        else:
            # Fallback to basic symptom extraction
            nlp = None
            logger.warning("Custom NER model not found, using fallback extraction")
        
        # Load sentence transformer
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("Loaded sentence transformer")
        
        # Initialize ChromaDB
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        
        # Try to get existing collection or create new one
        try:
            collection = client.get_collection("ayurveda_symptoms")
            logger.info("Loaded existing ChromaDB collection")
        except:
            # If collection doesn't exist, create it with sample data
            collection = client.create_collection("ayurveda_symptoms")
            logger.info("Created new ChromaDB collection")
            
            # Load sample data if available
            if os.path.exists("cleaned_ayurveda_data.json"):
                with open("cleaned_ayurveda_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                # Add data to collection
                for i, entry in enumerate(data[:100]):  # Limit to first 100 entries
                    symptoms_text = ", ".join(entry.get("symptoms", []))
                    if symptoms_text:
                        embedding = embedder.encode(symptoms_text).tolist()
                        collection.add(
                            embeddings=[embedding],
                            documents=[symptoms_text],
                            metadatas=[{
                                "disease": entry.get("disease", "Unknown"),
                                "dosha": ", ".join(entry.get("primary_dosha", [])),
                                "remedy": "; ".join(entry.get("remedies", [])[:3])  # Limit remedies
                            }],
                            ids=[f"entry_{i}"]
                        )
                logger.info("Populated ChromaDB with sample data")
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def extract_symptoms_fallback(text):
    """Fallback symptom extraction when NER model is not available"""
    # Common symptoms keywords
    symptom_keywords = [
        "headache", "stomachache", "nausea", "fever", "cough", "cold", "pain", 
        "ache", "sore", "tired", "fatigue", "dizzy", "bloating", "constipation",
        "diarrhea", "vomiting", "anxiety", "stress", "insomnia", "rash", "itching",
        "burning", "swelling", "inflammation", "congestion", "runny nose", "sneezing"
    ]
    
    text_lower = text.lower()
    found_symptoms = []
    
    for symptom in symptom_keywords:
        if symptom in text_lower:
            found_symptoms.append(symptom)
    
    return found_symptoms

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "AyurAI API is running"})

@app.route('/api/analyze-symptoms', methods=['POST'])
def analyze_symptoms():
    """Analyze symptoms and provide remedy recommendations"""
    try:
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return jsonify({"error": "No symptoms provided"}), 400
        
        user_input = data['symptoms']
        
        if not user_input.strip():
            return jsonify({"error": "Empty symptoms input"}), 400
        
        # Extract symptoms
        extracted_symptoms = []
        
        if nlp:
            # Use trained NER model
            doc = nlp(user_input)
            extracted_symptoms = [ent.text for ent in doc.ents if ent.label_ == "SYMPTOM"]
        else:
            # Use fallback extraction
            extracted_symptoms = extract_symptoms_fallback(user_input)
        
        if not extracted_symptoms:
            # If no specific symptoms found, use the entire input
            extracted_symptoms = [user_input]
        
        logger.info(f"Extracted symptoms: {extracted_symptoms}")
        
        # Query vector database
        if collection and embedder:
            query_text = ", ".join(extracted_symptoms)
            query_embedding = embedder.encode(query_text).tolist()
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=3
            )
            
            recommendations = []
            for i in range(len(results['documents'][0])):
                recommendation = {
                    "matched_symptoms": results['documents'][0][i],
                    "disease": results['metadatas'][0][i].get('disease', 'Unknown'),
                    "dosha": results['metadatas'][0][i].get('dosha', 'Unknown'),
                    "remedies": results['metadatas'][0][i].get('remedy', 'No remedies available'),
                    "confidence": 1.0 - (i * 0.1)  # Simple confidence scoring
                }
                recommendations.append(recommendation)
            
            return jsonify({
                "extracted_symptoms": extracted_symptoms,
                "recommendations": recommendations,
                "status": "success"
            })
        else:
            # Fallback response when models are not available
            return jsonify({
                "extracted_symptoms": extracted_symptoms,
                "recommendations": [{
                    "matched_symptoms": ", ".join(extracted_symptoms),
                    "disease": "General Health Concern",
                    "dosha": "Tridoshic",
                    "remedies": "Please consult with an Ayurvedic practitioner for personalized treatment. General recommendations include: maintain regular sleep schedule, eat warm cooked foods, practice gentle yoga, and stay hydrated.",
                    "confidence": 0.5
                }],
                "status": "fallback"
            })
            
    except Exception as e:
        logger.error(f"Error in analyze_symptoms: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/symptoms-suggestions', methods=['GET'])
def get_symptom_suggestions():
    """Get common symptom suggestions for autocomplete"""
    suggestions = [
        "headache", "stomach pain", "nausea", "fever", "cough", "cold symptoms",
        "fatigue", "dizziness", "bloating", "constipation", "diarrhea", "anxiety",
        "insomnia", "joint pain", "back pain", "sore throat", "runny nose",
        "skin rash", "itching", "burning sensation", "swelling", "congestion"
    ]
    
    return jsonify({"suggestions": suggestions})

if __name__ == '__main__':
    logger.info("Starting AyurAI Flask application...")
    
    # Load models on startup
    models_loaded = load_models()
    if not models_loaded:
        logger.warning("Some models failed to load, running with limited functionality")
    
    app.run(debug=True, host='0.0.0.0', port=5000)