# 🌏 Cultural Etiquette Advisor AI

**⚠️ For Evaluation / Portfolio Purposes Only ⚠️**

This project is a personal portfolio piece designed for technical assessment and recruiter review. The source code and assets are not licensed for public use, redistribution, or commercial deployment.

---

## ✨ Key Features

- **📍 Location-Aware Context**: Automatically detects locations in your queries and pulls relevant cultural data (Greetings, Dining, Business, Gifting) from a local database.
- **🤖 Hybrid AI Engine**: Combines a structured local knowledge base with the power of Large Language Models for accurate and nuanced responses.
- **💬 Chat History & Persistence**: Managed sessions with full history tracking, allowing you to resume conversations anytime.
- **🎨 Glassmorphism UI**: A modern, responsive interface featuring a sleek sidebar, typing indicators, and smooth message rendering.
- **🔒 Secure Authentication**: Built-in user registration and login system to keep your chat history private.
- **🚀 Advanced NLP**: Integrates `spacy` for sophisticated location extraction and intent recognition.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Django 5.1.x
- **Frontend**: Vanilla CSS (Glassmorphism), JavaScript (AJAX/Fetch API)
- **AI/LLM**: Meta Llama 3.1 (via NVIDIA API), Google Gemini (Optional Fallback)
- **Database**: SQLite (Development) / MySQL (Production Ready)
- **NLP**: Spacy, Regex
- **Environment**: python-dotenv for secure key management

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ installed
- A Virtual Environment (recommended)

### 2. Clone the Repository
```bash
git clone https://github.com/niranjanabaalu/cultural-etiquette-advisor-ai.git
cd cultural-etiquette-advisor-ai
```

### 3. Install Dependencies
```bash
# It is recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r cultural_advisor/requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the `cultural_advisor/` directory:
```env
NVIDIA_API_KEY=your_nvidia_api_key_here
# Optional if using Gemini fallback
# GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Setup Database
```bash
cd cultural_advisor
python manage.py migrate
python populate_db.py  # Optional: Populate the DB with initial cultural data
```

### 6. Run the Application
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 📁 Project Structure

```text
├───cultural_advisor          # Main Django Project Root
│   ├───advisor               # Main App (Logic, Views, Models)
│   │   ├───static/advisor    # Frontend Assets (CSS, JS)
│   │   ├───templates/advisor # HTML Templates
│   │   ├───gemini_service.py # AI Integration Logic
│   │   └───nlp_engine.py      # Location Detection Logic
│   ├───cultural_advisor      # Project Settings
│   │   └───settings.py
│   └───manage.py
├───.env                       # Environment Secrets (Ignored)
└───.gitignore                 # Git Exclusions
```

---

## 📝 Usage Tips
- **Be Specific**: Ask "What is the business etiquette in Japan?" for the most detailed response.
- **General Queries**: The bot also handles general cultural questions like "How do I greet people in various cultures?"
- **History**: Use the sidebar to browse through your previous chat sessions.

---

## 🤝 Contributing
Contributions are welcome! If you have suggestions for new features or localized etiquette data, please:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License & Usage
**All Rights Reserved.**

This repository is provided strictly for review by recruiters and hiring managers. No part of this project may be copied, redistributed, or used for any other purpose without the express written permission of the author.

---

**Built with ❤️ for Global Understanding.**
