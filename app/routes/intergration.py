from flask import Blueprint , request, jsonify
import requests 
from requests.auth import HTTPBasicAuth

from services.classification.zero_shot_classifier import classify
from services.description.description_generator import generate_description


integration_bp = Blueprint('integration', __name__)

@integration_bp.route('/woo_commerce/add_product', methods=['POST'])
def create_woo_commerce_product() : 
    
    product_name = request.json.get('productName')
    classification = classify(product_name=product_name)
    attr = ["White", "Leather", "Unisex", "Classic design"]
    description = generate_description(product_name , category=classification["category"] , attributes=attr )
    product_data = {
        "product_name" : product_name , 
        "category" : classification["category"] , 
        "description" :  description , 
        "image_url" : None
    }

    #return jsonify({"category" : classification , "desc" : description})


    domain = request.json.get('domain')
    customer_key = request.json.get('customer_key')
    customer_secret = request.json.get('customer_secret')

    url = f"{domain}/wp-json/wc/v3/products"
    auth = HTTPBasicAuth(customer_key, customer_secret)
    response = requests.post(url, json=product_data, auth=auth)
    if (response.status_code == 201) : 
        return jsonify({
            "message" : "Product created successfully",
            "product" : response.json()
        }) , 201
    else : 
        return jsonify({"error" : response.json() }) , response.status_code
    

@integration_bp.route('/custom_site/add_product', methods=['POST'])
def create_custom_site_product() : 
    

    pass