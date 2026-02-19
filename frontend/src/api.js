import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

export async function fetchQuestions() {
  const res = await api.get('/questions');
  return res.data;
}

export async function submitAnswers(data) {
  const res = await api.post('/submit', data);
  return res.data;
}

export async function getResult(sessionId) {
  const res = await api.get(`/result/${sessionId}`);
  return res.data;
}

export async function getScatterData() {
  const res = await api.get('/scatter-data');
  return res.data;
}

export function getExportUrl(sessionId) {
  return `/api/export/${sessionId}`;
}

export async function getAIReport(sessionId) {
  const res = await api.post(`/ai-report/${sessionId}`);
  return res.data;
}
