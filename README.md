# AyurAI - Ayurvedic Health Assistant

A modern web application that combines ancient Ayurvedic wisdom with AI technology to provide personalized health recommendations based on patient symptoms.

## Features

- **AI-Powered Symptom Analysis**: Advanced NLP models extract and analyze symptoms from natural language input
- **Ayurvedic Recommendations**: Get personalized remedies based on traditional Ayurvedic principles
- **Dosha Classification**: Understand your constitutional type (Vata, Pitta, Kapha) for targeted treatment
- **Modern UI/UX**: Beautiful, responsive interface with smooth animations
- **Real-time Analysis**: Instant symptom processing with confidence scoring
- **Autocomplete Suggestions**: Smart symptom suggestions to help users describe their conditions

## Technology Stack

### Backend
- **Flask**: Python web framework for the API
- **spaCy**: Natural Language Processing for symptom extraction
- **ChromaDB**: Vector database for similarity search
- **Sentence Transformers**: Text embeddings for semantic matching
- **CORS**: Cross-origin resource sharing support

### Frontend
- **React 18**: Modern React with hooks and functional components
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Framer Motion**: Smooth animations and transitions
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API communication

## Prerequisites

- Python 3.8+ with pip
- Node.js 16+ with npm
- Git

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ayur-ai
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# If you have the trained models, place them in the project root:
# - symptom_ner_model/ (spaCy NER model)
# - cleaned_ayurveda_data.json (processed dataset)
```

### 3. Frontend Setup
```bash
# Install Node.js dependencies
npm install
```

### 4. Running the Application

#### Start the Backend (Terminal 1)
```bash
python app.py
```
The Flask API will run on `http://localhost:5000`

#### Start the Frontend (Terminal 2)
```bash
npm start
```
The React app will run on `http://localhost:3000`

## Usage

1. **Open the Application**: Navigate to `http://localhost:3000` in your browser
2. **Describe Symptoms**: Enter your symptoms in natural language in the text area
3. **Get Recommendations**: Click "Analyze Symptoms" to receive AI-powered recommendations
4. **Review Results**: View extracted symptoms, matched conditions, dosha classifications, and remedies
5. **Follow Guidance**: Use the provided Ayurvedic remedies and lifestyle recommendations

## API Endpoints

### `GET /api/health`
Health check endpoint to verify server status.

### `POST /api/analyze-symptoms`
Analyze patient symptoms and return recommendations.

**Request Body:**
```json
{
  "symptoms": "I have headache and stomach pain"
}
```

**Response:**
```json
{
  "extracted_symptoms": ["headache", "stomach pain"],
  "recommendations": [
    {
      "disease": "Digestive Imbalance",
      "dosha": "Pitta",
      "remedies": "Drink warm water with ginger...",
      "confidence": 0.85,
      "matched_symptoms": "headache, abdominal discomfort"
    }
  ],
  "status": "success"
}
```

### `GET /api/symptoms-suggestions`
Get common symptom suggestions for autocomplete.

## Project Structure

```
ayur-ai/
├── app.py                 # Flask backend API
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind CSS configuration
├── public/
│   └── index.html        # HTML template
├── src/
│   ├── components/       # React components
│   │   ├── Header.jsx
│   │   ├── SymptomInput.jsx
│   │   └── RemedyResults.jsx
│   ├── services/
│   │   └── api.js        # API service layer
│   ├── App.js           # Main React component
│   ├── index.js         # React entry point
│   └── index.css        # Global styles
└── README.md
```

## Features Explained

### Symptom Analysis
The application uses a multi-step process:
1. **NLP Processing**: Extract symptoms from natural language using spaCy NER
2. **Semantic Matching**: Use sentence embeddings to find similar symptom patterns
3. **Vector Search**: Query ChromaDB for the most relevant Ayurvedic conditions
4. **Confidence Scoring**: Rank recommendations by similarity and relevance

### Ayurvedic Integration
- **Dosha Classification**: Recommendations are categorized by Vata, Pitta, and Kapha doshas
- **Traditional Remedies**: Suggestions include herbs, lifestyle changes, and dietary recommendations
- **Holistic Approach**: Focus on root cause treatment rather than symptom suppression

### User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Feedback**: Instant visual feedback during analysis
- **Accessibility**: Proper contrast ratios and keyboard navigation support
- **Error Handling**: Graceful degradation when services are unavailable

## Development Notes

### Model Integration
The application is designed to work with or without the trained AI models:
- **With Models**: Full AI-powered symptom extraction and matching
- **Without Models**: Fallback to keyword-based extraction and general recommendations

### Customization
- **Styling**: Modify `tailwind.config.js` and `src/index.css` for custom themes
- **API Endpoints**: Extend `app.py` to add new functionality
- **Components**: Add new React components in `src/components/`

## Deployment

### Backend Deployment
```bash
# Using Gunicorn for production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve static files with any web server
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Disclaimer

This application is for educational and informational purposes only. It is not intended to diagnose, treat, cure, or prevent any disease. Always consult with qualified healthcare professionals for medical advice and treatment.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the development team.