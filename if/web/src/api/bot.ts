// src/api/bot.ts

export const getBotStatus = async () => {
  const res = await fetch("/admin/bot/status");
  return res.json();
};

export const toggleAutoReply = async (enabled: boolean) => {
  const res = await fetch("/admin/bot/auto-reply", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enabled }),
  });
  return res.json();
};

export const triggerTrain = async () => {
  const res = await fetch("/debug/train", { method: "POST" });
  return res.json();
};