const sendBtn = document.getElementById ("sendBtn");
const userInput = document.getElementById("userInput");
const chatBody = document.getElementById("chatBody");
const autoSwitch = document.getElementById("autoSwitch");

function addMessage(content, sender = "user") {
  const msg = document.createElement("div");
  msg.className = `message ${sender === "user" ? "user-msg" : "bot-msg"} p-2 rounded shadow max-w-[75%] ${sender === "user" ? "bg-blue-100 self-end" : "bg-white self-start"}`;
  msg.innerHTML = marked.parse(content);
  chatBody.appendChild(msg);
  chatBody.scrollTop = chatBody.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";
  userInput.focus();

  if (!autoSwitch.checked) return;

  addMessage("...", "bot");

  try {
    const res = await fetch("/chat/generate-reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, user_id: "local_user" })
    });
    const data = await res.json();
    const lastBotMsg = chatBody.querySelector(".bot-msg:last-child");
    if (lastBotMsg) lastBotMsg.remove();
    addMessage(data.reply || "⚠️ No response.", "bot");
  } catch (error) {
    const lastBotMsg = chatBody.querySelector(".bot-msg:last-child");
    if (lastBotMsg) lastBotMsg.remove();
    addMessage("⚠️ Error: Could not connect to server.", "bot");
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});