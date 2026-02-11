import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generateCampaign = async (campaignData) => {
  try {
    const response = await api.post('/campaign/generate', campaignData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error('Network Error');
  }
};

export const generatePitch = async (pitchData) => {
  try {
    const response = await api.post('/pitch/generate', pitchData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error('Network Error');
  }
};

export const scoreLead = async (leadData) => {
  try {
    const response = await api.post('/lead/score', leadData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error('Network Error');
  }
};

