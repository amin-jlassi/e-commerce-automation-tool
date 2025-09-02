from app import Products, db
from flask import Blueprint , request, jsonify
from app.utils.response import to_dict
from sqlalchemy import text

classification_bp = Blueprint('classification', __name__)

@classification_bp.route('/categorys/', methods=['GET'])
def fetch_categories():
    query = text("SELECT DISTINCT(category) FROM products ;")
    categories = db.session.execute(query).fetchall()
    return jsonify({'categories': [category[0] for category in categories]}) , 200

