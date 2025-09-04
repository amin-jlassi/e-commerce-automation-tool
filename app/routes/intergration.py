from flask import Blueprint , request, jsonify
import requests 
from requests.auth import HTTPBasicAuth

from services.classification.zero_shot_classifier import classify


integration_bp = Blueprint('integration', __name__)

@integration_bp.route('/woo_commerce/add_product', methods=['POST'])
def create_woo_commerce_product() : 
    
    product_data = None


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