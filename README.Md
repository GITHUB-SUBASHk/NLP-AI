# 🤖 AI-RTCA — AI-Augmented Chat Assistant (Enterprise Edition)

AI-RTCA is a hybrid, privacy-preserving chat platform enhanced by local and remote AI (Rasa NLP) to provide emotionally intelligent, tone-sensitive replies.

---

## 🔧 Features

- ✨ Dual-mode AI: Local NLP and optional Rasa core
- 🧠 Memory-based interaction with tone & style analysis
- 🔒 Privacy-first design (local masking & anonymization)
- ⚡ FastAPI backend with WebSocket and REST
- 🌐 Clean web frontend with Tailwind CSS
- ✅ Auto-AI Reply toggle for controlled interaction

---

## 🚀 Getting Started

```bash
git clone https://github.com/github-SUBASHk/AI-rtca.git
cd AI-rtca
cp .env.example .env
pip install -r requirements.txt

##START SERVER
uvicorn interfaces.api_server.main:app --host 0.0.0.0 --port 8000 --reload

🤝 Contributing

Work-in-progress. 
All commits follow a modular update pattern.


#docker is to setup later
## 🛡️ License

This project is licensed under the **Polyform Shield License 1.0.0**.  
It is publicly visible **for deployment and collaboration purposes only**.

You **may not** use this code in production, redistribute it, or offer it as a service without explicit permission.

📄 Read more: [Polyform Shield License](https://polyformproject.org/licenses/shield/1.0.0/) Built with ❤️ by K Subash