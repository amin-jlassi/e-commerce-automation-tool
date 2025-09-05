import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os
import json
import dotenv
from openai import OpenAI
from PIL import Image
import io
import base64

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

def get_suitable_processed_image(product_name, min_width=800, upscale_factor=2, max_size=50 * 1024 * 1024):  # 50MB, adjust as needed (user might mean 50KB?)
    """
    Get a suitable processed image as base64 data URL.
    
    Args:
        product_name (str): Name of the product
        min_width (int): Minimum width before upscaling (default: 800)
        upscale_factor (int): Factor to upscale if below min_width (default: 2)
        max_size (int): Maximum file size in bytes (default: 50MB)
    
    Returns:
        str: Data URL of the processed image or original URL if processing fails, or None if no image found
    """
    urls = get_original_image_urls(product_name, 5)
    for url in urls:
        if verify_image_url(url, product_name):
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    img = Image.open(io.BytesIO(resp.content))
                    
                    if img.width < min_width:
                        new_size = (img.width * upscale_factor, img.height * upscale_factor)
                        img = img.resize(new_size, Image.LANCZOS)
                   
                    quality = 95
                    while True:
                        bio = io.BytesIO()
                        img.save(bio, 'JPEG', quality=quality)
                        data = bio.getvalue()
                        if len(data) <= max_size or quality < 20:
                            break
                        quality -= 5
                    
                    b64 = base64.b64encode(data).decode('utf-8')
                    return f"data:image/jpeg;base64,{b64}"
            except Exception as e:
                print(f"Error processing image {url}: {e}")
                
    if urls:
        return urls[0]
    return None