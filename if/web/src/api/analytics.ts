// src/api/analytics.ts

export const getBotConfidence = async () => {
  const res = await fetch("/analytics/stats");
  return res.json();
};