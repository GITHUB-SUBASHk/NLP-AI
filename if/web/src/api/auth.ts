import axios from "axios";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function loginUser(email: string, password: string) {
  const res = await axios.post(`${API}/auth/login`, { email, password });
  return res.data;
}