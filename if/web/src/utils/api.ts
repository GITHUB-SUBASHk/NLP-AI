import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL ||
 "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
});

// Fallbacks
export async function fetchRecentFallbacks() {
  const res = await api.get("/debug/fallbacks");
  return res.data;
}

// Analytics
export async function fetchConfidenceStats() {
  const res = await api.get("/analytics/stats");
  return res.data;
}

// Bot Status
export async function fetchBotStats() {
  const res = await api.get("/debug/stats");
  return res.data;
}

// Trigger train
export async function triggerTraining() {
  const res = await api.post("/debug/train");
  return res.data;
}