# Project Upgrade: Hybrid AI Cultural Advisor

The "AI Cultural Etiquette Advisor System" has been upgraded to a professional, hybrid architecture. This system now intelligently combines a **Rule-based Expert System (MySQL)** with the **Google Gemini API** for dynamic, context-aware responses.

## Key Improvements

### 1. Hybrid Architecture & Logic
- **Primary Stage (Expert System)**: The system first queries your local MySQL database for specific cultural etiquette rules (greetings, dining, dress code, etc.).
- **Secondary Stage (Gemini API)**: If no specific rules are found in the database, the system automatically falls back to the **Gemini-1.5-Flash** model to generate a natural language response.
- **Caching Layer**: To save time and API costs, repeated queries are stored in a local memory cache for 1 hour.

### 2. Expert System Extensibility
- **Django Admin**: You can now manage all cultural rules (add, edit, delete) directly through the Django Admin interface (`/admin`).
- **Database Optimization**: Added database indexes to the `country` field to ensure near-instant lookups even as your data grows.

### 3. Production Features
- **MySQL Integration**: Migrated from SQLite to a robust MySQL configuration.
- **Environment Management**: Moved sensitive credentials (API keys, DB passwords) into a `.env` file.
- **Refined NLP**: Improved intent detection in `nlp_engine.py` to distinguish between "Database-ready" queries and "Natural Language" queries.

## Next Steps for Final Setup

> [!IMPORTANT]
> Since you are using a local MySQL instance and have a private API Key, you must follow these final steps to activate the system.

### 1. Update your `.env` File
I have created a template `.env` file in your root directory. Open it and fill in your actual MySQL credentials and Google API Key.
[Open .env](file:///d:/Niranj/cultural-advisor-ai/cultural_advisor/.env)

### 2. Run Database Migrations
After updating `.env`, run the following commands in your terminal to create the MySQL tables:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 3. (Optional) Re-populate the Database
Since we moved to MySQL, your previous SQLite data is not available. Run your population script to fill the MySQL database with your initial expert rules:
```powershell
python populate_db.py
python enhance_db.py
```

### 4. Create an Admin User
To manage cultural rules via the web interface, create a superuser:
```powershell
python manage.py createsuperuser
```

## Architecture Diagram (Text-based)
```text
[ User Query ] 
      |
      v
[ Expert System (MySQL) ] --(Data Found)--> [ Return Formatted Advice ]
      |
  (No Data)
      |
      v
[ Google Gemini API ] ----(Generates)-----> [ Return & Cache Response ]
```
