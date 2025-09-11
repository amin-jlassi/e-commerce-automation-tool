import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

def get_original_image_urls(product_name, num=5):
    """
    Scrape original image URLs for a product from Google Images.
    
    Args:
        product_name (str): Name of the product
        num (int): Number of URLs to return (default: 5)
    
    Returns:
        list: List of original image URLs
    """
    query = product_name.replace(" ", "+") + "+product+image"
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = []
        for a in soup.find_all('a', href=True):
            if a['href'].startswith('/imgres?'):
                try:
                    qs = parse_qs(urlparse(a['href']).query)
                    imgurl = qs['imgurl'][0]
                    urls.append(imgurl)
                    if len(urls) == num:
                        break
                except KeyError:
                    pass
        return urls
    except Exception as e:
        print(f"Error fetching images: {e}")
        return []

def verify_image_url(image_url, product_name):
    """
    Verify if the image is suitable for product showcase using OpenAI Vision.
    
    Args:
        image_url (str): URL of the image
        product_name (str): Name of the product
    
    Returns:
        bool: True if suitable, False otherwise
    """
    prompt = f"Does this image depict a {product_name} suitable for e-commerce product display? Respond with 'yes' or 'no' followed by a brief reason."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            max_tokens=50
        )
        content = response.choices[0].message.content.lower()
        return 'yes' in content.split()[0]
    except Exception as e:
        print(f"Error verifying image: {e}")
        return False

def get_suitable_processed_image(product_name):
    """
    Get a suitable image URL for the product.
    
    Args:
        product_name (str): Name of the product
    
    Returns:
        str: URL of the suitable image, or None if no suitable image is found
    """
    urls = get_original_image_urls(product_name, 5)
    for url in urls:
        if verify_image_url(url, product_name):
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                resp = requests.head(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    return url
            except Exception as e:
                print(f"Error checking image {url}: {e}")
    
    if urls:
        return urls[0]  # Fallback to the first URL if no suitable image is found
    return None
if __name__ == "__main__":
    product = "wireless headphones"
    image_url = get_suitable_processed_image(product)
    print(image_url)