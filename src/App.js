import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, Wifi, WifiOff, RefreshCw } from 'lucide-react';

import Header from './components/Header';
import SymptomInput from './components/SymptomInput';
import RemedyResults from './components/RemedyResults';
import { apiService } from './services/api';

import './index.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [extractedSymptoms, setExtractedSymptoms] = useState([]);
  const [error, setError] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [serverStatus, setServerStatus] = useState('checking');

  // Check server health on mount
  useEffect(() => {
    checkServerHealth();
    loadSuggestions();
  }, []);

  const checkServerHealth = async () => {
    try {
      await apiService.healthCheck();
      setServerStatus('online');
    } catch (error) {
      console.error('Server health check failed:', error);
      setServerStatus('offline');
    }
  };

  const loadSuggestions = async () => {
    try {
      const suggestionsList = await apiService.getSymptomSuggestions();
      setSuggestions(suggestionsList);
    } catch (error) {
      console.warn('Failed to load suggestions:', error);
    }
  };

  const handleSymptomSubmit = async (symptoms) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const analysisResults = await apiService.analyzeSymptoms(symptoms);
      setResults(analysisResults);
      setExtractedSymptoms(analysisResults.extracted_symptoms || []);
      
      // Scroll to results
      setTimeout(() => {
        const resultsElement = document.getElementById('results-section');
        if (resultsElement) {
          resultsElement.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
      
    } catch (error) {
      console.error('Analysis failed:', error);
      setError(error.message || 'Failed to analyze symptoms. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    setError(null);
    setResults(null);
    checkServerHealth();
  };

  const ServerStatusIndicator = () => (
    <div className="fixed top-4 right-4 z-50">
      <div className={`flex items-center space-x-2 px-3 py-2 rounded-full text-sm font-medium ${
        serverStatus === 'online' 
          ? 'bg-green-100 text-green-800' 
          : serverStatus === 'offline'
          ? 'bg-red-100 text-red-800'
          : 'bg-yellow-100 text-yellow-800'
      }`}>
        {serverStatus === 'online' ? (
          <>
            <Wifi className="w-4 h-4" />
            <span>Connected</span>
          </>
        ) : serverStatus === 'offline' ? (
          <>
            <WifiOff className="w-4 h-4" />
            <span>Offline</span>
          </>
        ) : (
          <>
            <RefreshCw className="w-4 h-4 animate-spin" />
            <span>Connecting...</span>
          </>
        )}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-ayur-50 via-white to-green-50">
      <ServerStatusIndicator />
      <Header />
      
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Discover Your Path to{' '}
            <span className="text-ayur-600">Holistic Wellness</span>
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Get personalized Ayurvedic recommendations based on your symptoms. 
            Our AI combines ancient wisdom with modern technology to guide your healing journey.
          </p>
        </motion.div>

        {/* Symptom Input Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mb-8"
        >
          <SymptomInput
            onSubmit={handleSymptomSubmit}
            loading={loading}
            suggestions={suggestions}
          />
        </motion.div>

        {/* Error Display */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="mb-8"
            >
              <div className="card bg-red-50 border-red-200">
                <div className="flex items-start space-x-3">
                  <AlertCircle className="w-6 h-6 text-red-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <h3 className="font-semibold text-red-800 mb-1">
                      Analysis Failed
                    </h3>
                    <p className="text-red-700 text-sm mb-3">
                      {error}
                    </p>
                    <button
                      onClick={handleRetry}
                      className="btn-secondary text-red-700 border-red-300 hover:border-red-400"
                    >
                      Try Again
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Loading State */}
        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="mb-8"
            >
              <div className="card text-center py-12">
                <div className="loading-spinner w-8 h-8 mx-auto mb-4"></div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  Analyzing Your Symptoms
                </h3>
                <p className="text-gray-600">
                  Our AI is processing your symptoms and finding the best Ayurvedic recommendations...
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results Section */}
        <div id="results-section">
          <AnimatePresence>
            {results && !loading && (
              <RemedyResults
                results={results}
                extractedSymptoms={extractedSymptoms}
              />
            )}
          </AnimatePresence>
        </div>

        {/* Information Cards */}
        {!results && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="grid md:grid-cols-3 gap-6 mt-12"
          >
            <div className="card text-center">
              <div className="w-12 h-12 bg-ayur-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🧠</span>
              </div>
              <h3 className="font-semibold text-gray-800 mb-2">AI-Powered Analysis</h3>
              <p className="text-gray-600 text-sm">
                Advanced machine learning models trained on traditional Ayurvedic knowledge
              </p>
            </div>

            <div className="card text-center">
              <div className="w-12 h-12 bg-ayur-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🌿</span>
              </div>
              <h3 className="font-semibold text-gray-800 mb-2">Ancient Wisdom</h3>
              <p className="text-gray-600 text-sm">
                Based on thousands of years of Ayurvedic principles and natural healing methods
              </p>
            </div>

            <div className="card text-center">
              <div className="w-12 h-12 bg-ayur-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">⚖️</span>
              </div>
              <h3 className="font-semibold text-gray-800 mb-2">Dosha Balance</h3>
              <p className="text-gray-600 text-sm">
                Personalized recommendations based on your unique constitutional type
              </p>
            </div>
          </motion.div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600 text-sm">
            <p className="mb-2">
              © 2024 AyurAI. Combining ancient Ayurvedic wisdom with modern AI technology.
            </p>
            <p>
              <strong>Disclaimer:</strong> This tool is for educational purposes only and should not replace professional medical advice.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;