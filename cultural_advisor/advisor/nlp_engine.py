import logging

logger = logging.getLogger(__name__)

# Try to load spacy, but gracefully skip if not available
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logger.warning(f"spacy not available: {e}. NLP features will be basic.")
    nlp = None


# ---------------------------
# GLOBAL LOCATIONS
# ---------------------------

KNOWN_LOCATIONS = [

        # India regions
        "india",
        "tamil nadu",
        "kerala",
        "karnataka",
        "andhra pradesh",
        "telangana",
        "delhi",
        "mumbai",
        "chennai",
        "kolkata",

        # Asia
        "japan",
        "china",
        "south korea",
        "north korea",
        "singapore",
        "malaysia",
        "thailand",
        "indonesia",
        "philippines",
        "vietnam",
        "sri lanka",
        "nepal",
        "bangladesh",
        "pakistan",

        # Middle East
        "uae",
        "dubai",
        "saudi arabia",
        "qatar",
        "oman",
        "kuwait",

        # Europe
        "france",
        "germany",
        "italy",
        "spain",
        "uk",
        "united kingdom",
        "england",
        "netherlands",
        "switzerland",

        # America
        "usa",
        "united states",
        "canada",
        "mexico",
        "brazil",

        # Oceania
        "australia",
        "new zealand",

        # Regions
        "south asia",
        "southeast asia",
        "europe",
        "asia",
        "middle east"
]

# ---------------------------
# LOCATION DETECTION
# ---------------------------

def extract_location(text):

    text_lower = text.lower()

    for loc in KNOWN_LOCATIONS:
        if loc in text_lower:
            return loc.title()

    # Fallback if spacy is not available
    if nlp is None:
        return None
    
    try:
        doc = nlp(text.title())
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC", "NORP"]:
                return ent.text
    except Exception as e:
        logger.warning(f"Error in spacy processing: {e}")

    return None


# ---------------------------
# MULTIPLE LOCATION DETECTION
# (Used for comparison feature)
# ---------------------------

def extract_multiple_locations(text):

    locations = []
    
    # Use spacy if available
    if nlp is not None:
        try:
            doc = nlp(text.title())
            for ent in doc.ents:
                if ent.label_ in ["GPE", "LOC", "NORP"]:
                    extracted = ent.text.title()
                    if extracted not in locations:
                        locations.append(extracted)
        except Exception as e:
            logger.warning(f"Error in spacy processing: {e}")
                
    # Always check known locations as fallback
    text_lower = text.lower()
    for loc in KNOWN_LOCATIONS:
        loc_title = loc.title()
        if loc in text_lower and loc_title not in locations:
            locations.append(loc_title)

    return locations


# ---------------------------
# ADVANCED INTENT DETECTION
# ---------------------------

# Keyword groups for priority matching
INTENT_GROUPS = {
    "marriage_dress": ["marriage dress", "wedding dress", "marriage etiquette", "wedding etiquette", "bride", "groom", "marriage", "wedding attire", "marriage outfit"],
    "traditional_food": ["traditional food", "national dish", "famous food", "local cuisine", "specialty", "popular food", "best food"],
    "eating_style": ["how to eat", "eating style", "dining manner", "table manner", "eating etiquette", "hands or fork", "wash hands"],
    "gift_culture": ["gift culture", "giving gift", "present etiquette", "gift giving", "what to gift", "souvenir", "gift"],
    "education_dress": ["school dress", "college dress", "university dress", "school uniform", "education attire", "academy dress"],
    "festival": ["festival", "celebration", "famous festival", "traditional event", "holiday", "ceremony"],
    "greeting": ["how to greet", "say hello", "hello", "hi", "greeting", "welcome", "say hi"],
    "dining": ["dining", "restaurant", "meal", "food etiquette", "eating out"],
    "dress": ["dress code", "what to wear", "clothing", "outfit", "attire", "apparel"],
    "business": ["business", "office", "meeting", "professional", "work culture"],
    "dos": ["do", "should i", "respectful", "allowed", "okay to"],
    "donts": ["dont", "avoid", "rude", "taboo", "disrespectful", "illegal"],
}

def detect_intent(text):
    text = text.lower()

    # 1. PRIORITY MATCHING: Check for multi-word phrases first
    for intent, keywords in INTENT_GROUPS.items():
        for word in keywords:
            if " " in word and word in text:
                return intent

    # 2. SECONDARY MATCHING: Check for single keywords
    for intent, keywords in INTENT_GROUPS.items():
        for word in keywords:
            if word in text:
                return intent

    # 3. FALLBACK: Use simple map if not caught by groups
    intent_map = {
        "overview": ["culture", "cultural", "etiquette", "tradition", "custom", "about", "overview", "tell me about", "guide"],
        "language": ["language", "speak", "talk"],
        "tourism": ["travel", "tourist", "visit", "trip"],
        "recommend": ["recommend", "suggest", "where should i"],
        "capital": ["capital"],
        "communication": ["communication", "talk to"],
    }

    for intent, keywords in intent_map.items():
        for word in keywords:
            if word in text:
                return intent

    # 4. FINAL FALLBACK: If no specific keywords, it's a 'natural' query for AI
    return "natural_language"