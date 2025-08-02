import React, { useState, useEffect, useRef } from 'react';
import { Send, Lightbulb, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const SymptomInput = ({ onSubmit, loading, suggestions = [] }) => {
  const [symptoms, setSymptoms] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState([]);
  const textareaRef = useRef(null);

  useEffect(() => {
    if (symptoms.length > 0) {
      const filtered = suggestions.filter(suggestion =>
        suggestion.toLowerCase().includes(symptoms.toLowerCase().split(' ').pop())
      );
      setFilteredSuggestions(filtered.slice(0, 6));
      setShowSuggestions(filtered.length > 0);
    } else {
      setShowSuggestions(false);
    }
  }, [symptoms, suggestions]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (symptoms.trim() && !loading) {
      onSubmit(symptoms.trim());
    }
  };

  const handleSuggestionClick = (suggestion) => {
    const words = symptoms.split(' ');
    words[words.length - 1] = suggestion;
    setSymptoms(words.join(' ') + ' ');
    setShowSuggestions(false);
    textareaRef.current?.focus();
  };

  const addCommonSymptom = (symptom) => {
    if (symptoms) {
      setSymptoms(symptoms + ', ' + symptom);
    } else {
      setSymptoms(symptom);
    }
    textareaRef.current?.focus();
  };

  const commonSymptoms = [
    'headache', 'stomach pain', 'fatigue', 'anxiety', 'insomnia', 'nausea'
  ];

  return (
    <div className="card relative">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-2">
          Describe Your Symptoms
        </h2>
        <p className="text-gray-600 text-sm">
          Tell us about what you're experiencing. Be as detailed as possible for better recommendations.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            ref={textareaRef}
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            placeholder="I have been experiencing headache and stomach pain for the past few days..."
            className="input-field min-h-[120px] resize-none"
            disabled={loading}
          />
          
          {/* Suggestions Dropdown */}
          <AnimatePresence>
            {showSuggestions && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto"
              >
                {filteredSuggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="w-full text-left px-4 py-2 hover:bg-ayur-50 transition-colors duration-150 first:rounded-t-lg last:rounded-b-lg"
                  >
                    <span className="text-sm text-gray-700">{suggestion}</span>
                  </button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Common Symptoms Quick Add */}
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Lightbulb className="w-4 h-4" />
            <span>Quick add common symptoms:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {commonSymptoms.map((symptom) => (
              <button
                key={symptom}
                type="button"
                onClick={() => addCommonSymptom(symptom)}
                disabled={loading}
                className="px-3 py-1 text-xs bg-ayur-100 text-ayur-700 rounded-full hover:bg-ayur-200 transition-colors duration-150 disabled:opacity-50"
              >
                + {symptom}
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-between items-center pt-4">
          <div className="text-sm text-gray-500">
            {symptoms.length}/500 characters
          </div>
          
          <div className="flex space-x-3">
            {symptoms && (
              <button
                type="button"
                onClick={() => setSymptoms('')}
                disabled={loading}
                className="btn-secondary flex items-center space-x-2"
              >
                <X className="w-4 h-4" />
                <span>Clear</span>
              </button>
            )}
            
            <button
              type="submit"
              disabled={!symptoms.trim() || loading}
              className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="loading-spinner w-4 h-4"></div>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Analyze Symptoms</span>
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default SymptomInput;