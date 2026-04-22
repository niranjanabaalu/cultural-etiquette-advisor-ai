# Cultural Etiquette Advisor AI

[![License: All Rights Reserved](https://img.shields.io/badge/License-AllRightsReserved-red.svg)](LICENSE)

> 🚫 **This project is intended for demonstration purposes only. Reuse, modification, or redistribution of this code is not permitted without written permission from the author.**

---

A sophisticated, location-aware AI chatbot developed as part of my BCA final year mini project using Django and advanced LLM integration.

![Project Banner](https://github.com/niranjanabaalu/cultural-etiquette-advisor-ai/raw/main/front_image.png)

---

## Overview

**Cultural Etiquette Advisor AI** is a professional web application designed to bridge cultural gaps and provide reliable etiquette advice for world travelers and business professionals. The system leverage a hybrid architecture: it uses a structured local database for country-specific etiquette and integrates the **Meta Llama 3.1** model (via NVIDIA AI) to provide nuanced, conversational responses based on real-time location detection.

---

## Tech Stack

- **Frontend**: HTML, Vanilla CSS (Glassmorphism), JavaScript (AJAX/Fetch)
- **Backend**: Python (Django Framework)
- **AI / LLM**: Meta Llama 3.1 (NVIDIA AI API), Google Gemini (Fallback)
- **Database**: SQLite (Development)
- **Core Features**: Location Extraction, Context-Aware Prompts, Chat History Management, Session Persistence, User Authentication

---

## Screenshots

### Login / Sign Up
![Login Page](https://github.com/niranjanabaalu/cultural-etiquette-advisor-ai/blob/main/login_page.JPG?raw=true)
![Signup Page](https://github.com/niranjanabaalu/cultural-etiquette-advisor-ai/blob/main/sign_up_page.JPG?raw=true)

### Home Page
![Home Page](https://github.com/niranjanabaalu/cultural-etiquette-advisor-ai/blob/main/home_page.JPG?raw=true)

### AI Chat Interface
![Chat Interface](https://github.com/niranjanabaalu/cultural-etiquette-advisor-ai/blob/main/chat_page.JPG?raw=true)
![Chat Message](https://github.com/niranjanabaalu/cultural-etiquette-advisor-ai/blob/main/advisor_chatmessage.JPG?raw=true)

### Bot Interaction
![Bot is Thinking](https://github.com/niranjanabaalu/cultural-etiquette-advisor-ai/blob/main/bot_is_thinking.JPG?raw=true)

---

## Key Features

- **Contextual Awareness**: Automatically identifies mentioned countries and provides specific data on Greetings, Dining, and Business etiquette.
- **Persistent Chat History**: Securely stores conversation sessions per user, allowing for multi-turn dialogue memory.
- **Modern UI/UX**: Implements a sleek Glassmorphism design with a responsive sidebar for session management.
- **Robust AI Integration**: Features intelligent retry logic, exponential backoff, and fallback systems for high availability.
- **Secure Authentication**: Built-in Django user management, ensuring data privacy and individual chat histories.

---

## Project Purpose

This project was developed as part of my final year BCA curriculum to showcase industrial-grade skills in full-stack development, AI API integration, and user-centric design. It demonstrates the ability to combine traditional relational databases with modern Large Language Models to solve real-world cross-cultural communication challenges.

---

## Future Enhancements

- **Voice Interaction**  
  Implement Speech-to-Text and Text-to-Speech for a truly hands-free advisor experience.

- **Interactive Maps**  
  Integrate Leaflet or Google Maps to allow users to click on regions for instant cultural tips.

- **Real-time Travel Alerts**  
  Add API integrations for current travel advisories, currency exchange rates, and local news.

---

## Developer

**Niranjana B**  
Email: [niranjanab005@gmail.com](mailto:niranjanab005@gmail.com)  
LinkedIn: [linkedin.com/in/niranjana-balasubramanian-1ab0a4251](https://linkedin.com/in/niranjana-balasubramanian-1ab0a4251)  
GitHub: [github.com/niranjanabaalu](https://github.com/niranjanabaalu)

---

*This project reflects my commitment to building intelligent, scalable, and visually impactful applications using the latest web and AI technologies.*
