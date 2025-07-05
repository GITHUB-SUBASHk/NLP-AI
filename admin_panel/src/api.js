import axios from "axios";

const api = axios.create({
  baseURL: "/debug", // Or "/" depending on your proxy
});

// Attach JWT from localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("jwt");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Trigger RASA training via API
export const triggerTraining = async () => {
  const res = await api.post("/train");
  return res.data;
};

export default api;