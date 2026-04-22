import requests
import logging
import traceback

logger = logging.getLogger(__name__)

def fetch_external_country_data(country_name):
    """
    Fetches dynamic country data from REST Countries API.
    Returns a dictionary with flag_url, official_name, capital, region, languages, currency, population.
    """
    if not country_name:
        return {'success': False, 'error': 'No country name provided'}

    try:
        # Use fullText=true for more accurate matching
        url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            # Try without fullText if not found (fuzzy match)
            url = f"https://restcountries.com/v3.1/name/{country_name}"
            response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data_list = response.json()
            if not data_list or not isinstance(data_list, list):
                return {'success': False, 'error': 'Invalid API response structure'}
                
            data = data_list[0]
            
            # Extract relevant fields safely
            languages_dict = data.get('languages', {})
            languages = ", ".join(languages_dict.values()) if languages_dict else "N/A"
            
            # Currency extraction safely
            currencies = data.get('currencies', {})
            currency_list = []
            if currencies:
                for code, info in currencies.items():
                    name = info.get('name', 'N/A')
                    symbol = info.get('symbol', '')
                    currency_list.append(f"{name} ({symbol})")
            currency_str = ", ".join(currency_list) if currency_list else "N/A"

            # Population formatting safety
            pop = data.get('population')
            pop_str = f"{pop:,}" if isinstance(pop, (int, float)) else "N/A"

            # Capital safety
            capitals = data.get('capital', [])
            capital_str = ", ".join(capitals) if capitals else "N/A"

            return {
                'flag_url': data.get('flags', {}).get('png'),
                'official_name': data.get('name', {}).get('official'),
                'capital': capital_str,
                'region': data.get('region', 'N/A'),
                'subregion': data.get('subregion', 'N/A'),
                'languages': languages,
                'currency': currency_str,
                'population': pop_str,
                'success': True
            }
        else:
            logger.warning(f"API returned status {response.status_code} for {country_name}")
    except Exception as e:
        logger.error(f"Error fetching country data for {country_name}: {e}\n{traceback.format_exc()}")
    
    return {'success': False, 'error': 'API request failed'}

def fetch_from_wikipedia(location, aspect):
    """
    Fetches a brief summary from Wikipedia for a specific cultural aspect of a location.
    Tries multiple query variations for better fallback.
    """
    headers = {
        'User-Agent': 'CulturalEtiquetteAdvisor/1.0 (Contact: contact@example.com)'
    }
    
    # Variations to try for better hits
    queries = [
        f"{aspect} in {location}",
        f"{location} {aspect}",
        f"{aspect} of {location}",
        f"Culture of {location}",
        location
    ]
    
    for query in queries:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_").replace("?", "")
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                extract = data.get('extract')
                if extract:
                    # Basic cleaning: remove parentheticals
                    import re
                    extract = re.sub(r'\([^)]*\)', '', extract).replace('  ', ' ')
                    return extract
        except Exception as e:
            logger.warning(f"Wikipedia fallback failed for {query}: {e}")
    
    return None

def merge_etiquette_data(db_data, api_data):
    """
    Intelligently merges database etiquette data with API country data.
    Returns a unified dictionary for the conversational engine.
    """
    country_name = 'the requested location'
    if db_data:
        country_name = db_data.country
    elif api_data.get('success'):
        country_name = api_data.get('official_name') or api_data.get('country')

    merged = {
        'country': country_name,
        'flag_url': api_data.get('flag_url') if api_data.get('success') else (db_data.flag_url if db_data else None),
        'capital': api_data.get('capital') if api_data.get('success') else (getattr(db_data, 'capital_city', 'N/A') if db_data else 'N/A'),
        'currency': api_data.get('currency') if api_data.get('success') else (getattr(db_data, 'currency', 'N/A') if db_data else 'N/A'),
        'population': api_data.get('population') if api_data.get('success') else (getattr(db_data, 'population', 'N/A') if db_data else 'N/A'),
        'official_name': api_data.get('official_name') if api_data.get('success') else (getattr(db_data, 'official_name', None) if db_data else None),
        'success': api_data.get('success', False) or (True if db_data else False),
        'has_culture': True if db_data else False
    }
    
    # Map all DB fields to common keys
    if db_data:
        merged.update({
            'cultural_overview': getattr(db_data, 'communication_style', ''),
            'greeting_word': getattr(db_data, 'greeting_word', ''),
            'greeting_gesture': getattr(db_data, 'greeting_gesture', ''),
            'dining_etiquette': getattr(db_data, 'dining_etiquette', ''),
            'dress_code': getattr(db_data, 'dress_code', ''),
            'business_etiquette': getattr(db_data, 'business_meeting', ''),
            'dos': getattr(db_data, 'dos', ''),
            'donts': getattr(db_data, 'donts', ''),
            
            # New fields
            'marriage_dress': getattr(db_data, 'marriage_dress', ''),
            'festival': getattr(db_data, 'famous_festivals', ''),
            'traditional_food': getattr(db_data, 'traditional_food', ''),
            'eating_style': getattr(db_data, 'eating_style', ''),
            'gift_culture': getattr(db_data, 'gift_culture_specific', '') or getattr(db_data, 'gift_giving', ''),
            'education_dress': getattr(db_data, 'education_dress', ''),
        })

    return merged
