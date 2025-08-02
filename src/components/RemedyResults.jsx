import React from 'react';
import { motion } from 'framer-motion';
import { 
  CheckCircle, 
  AlertCircle, 
  Sparkles, 
  Target,
  Clock,
  Star
} from 'lucide-react';

const RemedyResults = ({ results, extractedSymptoms }) => {
  if (!results || !results.recommendations) {
    return null;
  }

  const getDoshaClass = (dosha) => {
    const doshaLower = dosha.toLowerCase();
    if (doshaLower.includes('vata')) return 'dosha-vata';
    if (doshaLower.includes('pitta')) return 'dosha-pitta';
    if (doshaLower.includes('kapha')) return 'dosha-kapha';
    return 'bg-gray-100 text-gray-800';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceStars = (confidence) => {
    const stars = Math.round(confidence * 5);
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-4 h-4 ${
          i < stars ? 'text-yellow-400 fill-current' : 'text-gray-300'
        }`}
      />
    ));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Extracted Symptoms Summary */}
      <div className="card bg-ayur-50 border-ayur-200">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <CheckCircle className="w-6 h-6 text-ayur-600 mt-0.5" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-ayur-800 mb-2">
              Identified Symptoms
            </h3>
            <div className="flex flex-wrap gap-2">
              {extractedSymptoms.map((symptom, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-white text-ayur-700 rounded-full text-sm font-medium border border-ayur-200"
                >
                  {symptom}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* AI Recommendations */}
      <div className="space-y-4">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-6 h-6 text-ayur-600" />
          <h3 className="text-xl font-semibold text-gray-800">
            AI-Powered Recommendations
          </h3>
        </div>

        {results.recommendations.map((recommendation, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="card hover:shadow-xl transition-all duration-300"
          >
            <div className="space-y-4">
              {/* Header with confidence and dosha */}
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h4 className="text-lg font-semibold text-gray-800 mb-2">
                    {recommendation.disease}
                  </h4>
                  <div className="flex items-center space-x-3">
                    <span className={`dosha-badge ${getDoshaClass(recommendation.dosha)}`}>
                      {recommendation.dosha}
                    </span>
                    <div className="flex items-center space-x-1">
                      {getConfidenceStars(recommendation.confidence)}
                      <span className={`text-sm font-medium ml-2 ${getConfidenceColor(recommendation.confidence)}`}>
                        {Math.round(recommendation.confidence * 100)}% match
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex-shrink-0">
                  <div className={`w-3 h-3 rounded-full ${
                    index === 0 ? 'bg-green-400' : 
                    index === 1 ? 'bg-yellow-400' : 'bg-gray-400'
                  }`}></div>
                </div>
              </div>

              {/* Matched Symptoms */}
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Target className="w-4 h-4 text-gray-600" />
                  <span className="text-sm font-medium text-gray-700">
                    Similar Symptom Pattern
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  {recommendation.matched_symptoms}
                </p>
              </div>

              {/* Remedies */}
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Clock className="w-4 h-4 text-ayur-600" />
                  <span className="font-medium text-ayur-800">
                    Recommended Remedies
                  </span>
                </div>
                
                <div className="bg-gradient-to-r from-ayur-50 to-green-50 rounded-lg p-4 border-l-4 border-ayur-500">
                  <div className="prose prose-sm max-w-none">
                    {recommendation.remedies.split(';').map((remedy, remedyIndex) => (
                      <div key={remedyIndex} className="mb-2 last:mb-0">
                        <p className="text-gray-700 leading-relaxed">
                          • {remedy.trim()}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Disclaimer for lower confidence */}
              {recommendation.confidence < 0.7 && (
                <div className="flex items-start space-x-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                  <div className="text-sm text-yellow-800">
                    <strong>Note:</strong> This recommendation has lower confidence. 
                    Consider consulting with an Ayurvedic practitioner for personalized advice.
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        ))}
      </div>

      {/* General Disclaimer */}
      <div className="card bg-blue-50 border-blue-200">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-6 h-6 text-blue-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-blue-800">
            <strong className="block mb-1">Important Disclaimer</strong>
            These recommendations are based on traditional Ayurvedic principles and AI analysis. 
            They are not a substitute for professional medical advice. Please consult with qualified 
            healthcare practitioners for serious health concerns.
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default RemedyResults;