import requests 
from requests.auth import HTTPBasicAuth



def create_woo_commerce_product(product_data , domain , customer_key , customer_secret) : 
    url = f"{domain}/wp-json/wc/v3/products"
    auth = HTTPBasicAuth(customer_key, customer_secret)
    response = requests.post(url, json=product_data, auth=auth)
    if (response.status_code == 201) : 
        return response.json()
    else : 
        return {"error" : response.json() }