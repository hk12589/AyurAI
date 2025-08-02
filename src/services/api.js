import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/api/health');
      return response.data;
    } catch (error) {
      throw new Error('Failed to connect to server');
    }
  },

  // Analyze symptoms
  analyzeSymptoms: async (symptoms) => {
    try {
      const response = await api.post('/api/analyze-symptoms', {
        symptoms: symptoms.trim(),
      });
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Failed to analyze symptoms. Please try again.');
    }
  },

  // Get symptom suggestions
  getSymptomSuggestions: async () => {
    try {
      const response = await api.get('/api/symptoms-suggestions');
      return response.data.suggestions || [];
    } catch (error) {
      console.warn('Failed to load symptom suggestions:', error);
      return [];
    }
  },
};

export default apiService;