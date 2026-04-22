# Cultural Advisor AI Project Documentation

## Overview

This project is a Django-based web application that provides a conversational Cultural Etiquette Advisor. It allows registered users to chat with an AI-powered assistant that answers culture, etiquette, travel, greeting, dining, and business behavior questions for countries and regions.

The application stores chat sessions and messages in a local SQLite database and uses an external AI model API to generate responses.

## Main Components

### Django App

- Project root: `cultural_advisor/`
- Main app: `advisor/`
- Database: SQLite (`db.sqlite3`)
- Templates: `advisor/templates/advisor/`
- Static assets: `advisor/static/advisor/`

### Core Models

- `Etiquette`
  - Stores country-specific cultural data.
  - Fields include greeting, dining etiquette, business etiquette, dress code, gift giving, dos/donts, language, festivals, traditional food, and tourism tips.
  - Includes auxiliary fields such as `flag_url`, `official_name`, `population`, and `currency`.
- `ChatSession`
  - Stores conversation sessions per user.
  - Tracks creation and update timestamps, session title, and optional metadata like `flag_sent` and `last_country`.
- `ChatMessage`
  - Stores individual user and bot messages.
  - Tracks whether a message is from the bot (`is_bot`) and the timestamp.
- `APILog`
  - Tracks external API calls for debugging and monitoring.
  - Supports `GEMINI`, `REST_COUNTRIES`, and `WIKIPEDIA` API types.

## Functionality and Workflow

### User Authentication

- Users can sign up using `signup_view`.
- Users can log in using `login_view`.
- Users can log out using `logout_view`.
- Access to the main chat interface is protected by `@login_required`.

### Chatbot API

- Endpoint: `POST /chat/`
- The chat endpoint accepts JSON with `message` and optional `session_id`.
- If the request is not `POST`, it returns `405 Method not allowed`.
- If the message is empty, it returns `400 Empty message`.
- It attempts to detect a location from the user message and loads related `Etiquette` data if available.
- Creates or reuses a `ChatSession` for the current user.
- Saves the user message as a `ChatMessage`.
- Sends the prompt to the external AI service and saves the response as a bot message.
- Returns JSON containing `reply` and `session_id`.

### Location and Context Extraction

- The app detects locations in user messages via `advisor/nlp_engine.py`.
- Location detection is based on a hard-coded `KNOWN_LOCATIONS` list.
- If `spacy` is installed and available, it can also use named entity recognition to detect locations.
- When an identified location matches an `Etiquette` record, the bot builds context including:
  - Greeting customs
  - Dining etiquette
  - Business etiquette
  - Dress code
  - Gift giving
  - Do's and Dont's
- This cultural context is prepended to the AI prompt to provide more accurate, country-aware replies.

### AI Response Generation

- The AI integration is implemented in `advisor/gemini_service.py`.
- It uses NVIDIA’s API endpoint: `https://integrate.api.nvidia.com/v1/chat/completions`.
- The configured model is `meta/llama-3.1-70b-instruct`.
- It sends a system prompt telling the model to act as a cultural etiquette advisor.
- The AI call includes retry logic for HTTP errors and rate limiting:
  - Retries up to 3 times.
  - Uses exponential backoff on rate limit responses.
  - Handles timeout, request, and generic exceptions.
- If no `NVIDIA_API_KEY` is found, it returns an error message instead of sending the request.

## Frontend Behavior

### Main chat page

- Template: `advisor/templates/advisor/index.html`
- Loads static CSS and JavaScript.
- Displays a sidebar with chat history, session switching, and logout.
- Shows a chat window with bot and user messages.
- Includes an input field and send button.

### JavaScript chat logic

- Script: `advisor/static/advisor/js/chat.js`
- Loads chat history from `GET /history/`.
- Allows selecting a previous session and loading its messages.
- Sends new messages via `POST /chat/`.
- Displays a typing indicator while waiting for the bot response.
- Appends chat bubbles for user and bot messages.
- Updates `currentSessionId` when message replies arrive.
- Refreshes session history after each message.
- Provides a simple markdown parser for bot responses, handling:
  - headers
  - bold text
  - images
  - line breaks
  - horizontal rules

## History and Session Management

- Endpoint: `GET /history/`
  - Returns the current user’s chat sessions sorted by most recent update.
  - Each session includes `id`, `title`, and `timestamp`.
- Endpoint: `GET /messages/<session_id>/`
  - Returns all messages for a given session.
- Endpoint: `GET /delete-session/<session_id>/`
  - Deletes a chat session for the current user.

## Routing

- App URLs are defined in `advisor/urls.py`:
  - `/` → `home`
  - `/chat/` → `chatbot`
  - `/signup/` → `signup_view`
  - `/login/` → `login_view`
  - `/logout/` → `logout_view`
  - `/history/` → `get_chat_history`
  - `/messages/<session_id>/` → `get_session_messages`
  - `/delete-session/<session_id>/` → `delete_chat_session`
- Root URL config in `cultural_advisor/urls.py` includes the `advisor` app and admin.

## Key Features

- Authenticated cultural advisor chat experience
- Persistent chat sessions per user
- Message history and session switching
- Location-aware cultural context using country etiquette data
- AI response generation via NVIDIA integration
- Retry and error handling for AI API requests
- Optional NLP enhancements with `spacy` if installed
- Extensible country etiquette model for greeting, dining, business, dress, gifting, festivals, food, and tourism
- Simple responsive UI with history sidebar and chat bubble rendering

## Important File Locations

- `cultural_advisor/cultural_advisor/settings.py` — Django settings and NVIDIA API config
- `cultural_advisor/advisor/views.py` — Request handling, chat API, auth, history endpoints
- `cultural_advisor/advisor/models.py` — Data definitions for etiquette, chat sessions, and messages
- `cultural_advisor/advisor/gemini_service.py` — AI API integration and retry handling
- `cultural_advisor/advisor/nlp_engine.py` — Location extraction and intent detection
- `cultural_advisor/advisor/static/advisor/js/chat.js` — Client-side chat UI and AJAX logic
- `cultural_advisor/advisor/templates/advisor/index.html` — Main chat page layout

## Dependencies and Setup Notes

- This app uses Django 5.1.4.
- Dependencies are listed in `cultural_advisor/requirements.txt`.
- The app expects an environment variable `NVIDIA_API_KEY` loaded via `.env`.
- `DEBUG = True` in settings, so this is configured for development.
- Database is SQLite by default.

## How to Run

1. Install dependencies: `pip install -r cultural_advisor/requirements.txt`
2. Create or update `.env` with `NVIDIA_API_KEY=your_api_key`
3. Run migrations: `python cultural_advisor/manage.py migrate`
4. Start the server: `python cultural_advisor/manage.py runserver`
5. Open the browser at `http://127.0.0.1:8000/`

## Notes

- The current AI integration uses NVIDIA’s hosted chat completion API, not the Google Gemini SDK.
- The code includes a commented optional Gemini API implementation.
- Location detection is currently based on a fixed list of known locations, with `spacy` as a fallback when available.
- The `Etiquette` model is designed for broad cultural content and can be populated through Django admin or custom scripts.

---

This documentation reflects the actual implementation and runtime behavior in the current repository state.
