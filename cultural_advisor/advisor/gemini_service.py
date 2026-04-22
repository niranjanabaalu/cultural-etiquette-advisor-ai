import time
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

def get_gemini_response_with_retry(prompt, max_retries=3):
    """
    Calls NVIDIA AI API with improved retry logic, error handling, and logging.
    """
    api_key = getattr(settings, 'NVIDIA_API_KEY', None)
    logger.info(f"NVIDIA API Key loaded: {'Yes' if api_key else 'No'}")
    if not api_key:
        logger.error("NVIDIA_API_KEY not found in settings")
        return "I'm sorry, but my AI service is currently unavailable. Please try again later."

    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [
            {
                "role": "system", 
                "content": (
                    "You are a professional Cultural Etiquette Advisor. "
                    "Provide comprehensive and professional responses. "
                    "Use structured bullet points for readability. Organize information into clear, punchy points with brief explanations. "
                    "If the user's location is known, personalize the response for that specific country or region."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Attempting NVIDIA API call (attempt {attempt + 1}/{max_retries + 1})")
            response = requests.post(url, headers=headers, json=data, timeout=120)  # Increased timeout for large model
            logger.info(f"API Response Status: {response.status_code}")
            logger.debug(f"API Response Body: {response.text}")

            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and result['choices'] and 'message' in result['choices'][0]:
                    content = result['choices'][0]['message']['content'].strip()
                    if content:
                        logger.info(f"API call successful. Response length: {len(content)} characters.")
                        return content
                    else:
                        logger.warning("API returned empty content")
                        return "I apologize, but I couldn't generate a response right now. Please try rephrasing your question."
                else:
                    logger.error(f"Unexpected API response structure: {result}")
                    return "I'm having trouble processing your request. Please try again."
            elif response.status_code == 429:
                logger.warning(f"Rate limit hit (attempt {attempt + 1})")
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time} seconds")
                    time.sleep(wait_time)
                    continue
                else:
                    return "I'm currently receiving too many requests. Please wait a moment and try again."
            elif response.status_code == 401:
                logger.error("Invalid API key")
                return "There's an issue with my configuration. Please contact support."
            elif response.status_code == 404:
                logger.error("Model not found")
                return "The AI model I'm trying to use isn't available right now."
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                if attempt < max_retries:
                    time.sleep(1)
                    continue
                else:
                    return "I'm experiencing technical difficulties. Please try again in a few minutes."
        except requests.exceptions.Timeout:
            logger.error(f"API Timeout (attempt {attempt + 1})")
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                return "The request took too long. Please try again."
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error (attempt {attempt + 1}): {e}")
            if attempt < max_retries:
                time.sleep(1)
                continue
            else:
                return "I'm having trouble connecting to my AI service. Please check your internet and try again."
        except Exception as e:
            logger.error(f"Unexpected Error (attempt {attempt + 1}): {e}")
            return "An unexpected error occurred. Please try again."

    return "I'm sorry, but I'm unable to provide a response right now. Please try again later."


# Optional: Alternative implementation using Google Gemini API
# Uncomment and install google-genai if switching to Gemini
# pip install google-genai

# from google import genai

# def get_gemini_response_gemini_api(prompt):
#     """
#     Alternative implementation using Google Gemini API.
#     Requires GOOGLE_API_KEY in .env and google-genai installed.
#     """
#     google_api_key = getattr(settings, 'GOOGLE_API_KEY', None)
#     if not google_api_key:
#         logger.error("GOOGLE_API_KEY not found")
#         return "AI service unavailable."
#     
#     try:
#         client = genai.Client(api_key=google_api_key)
#         response = client.models.generate_content(
#             model="gemini-2.0-flash-exp",
#             contents=f"You are a Cultural Etiquette Advisor. Answer naturally: {prompt}"
#         )
#         return response.text.strip() if response.text else "No response generated."
#     except Exception as e:
#         logger.error(f"Gemini API Error: {e}")
#         return "AI service error."