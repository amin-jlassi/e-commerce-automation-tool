import requests
import os
from  dotenv import load_dotenv

load_dotenv()



def fetch_categories():

    response = requests.get(f"{os.getenv('base_url')}/classification/categorys/")
    if response.status_code == 200 : 
        return response.json()
    return {'categories': []}
