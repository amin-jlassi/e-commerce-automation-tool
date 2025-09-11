import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("google_search_api_key")
SEARCH_ENGINE_ID = os.getenv("seach_engine_id")
def google_search_api(api_key, search_engine_id, query, num=5):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "searchType": "image",
        "num": num
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def fetch_image(product_name, num=5):
    result = google_search_api(API_KEY, SEARCH_ENGINE_ID, "air force nike air", 3)
    images = [item['link'] for item in result.get("items")]
    return images

if __name__ == "__main__":
    images = fetch_image("air force nike air", 3)
    print(images[0])