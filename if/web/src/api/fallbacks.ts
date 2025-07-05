// src/api/fallbacks.ts

export const getRecentFallbacks = async () => {
  const res = await fetch("/debug/fallbacks");
  return res.json();
};