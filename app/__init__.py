from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import os 
from dotenv import load_dotenv
    
load_dotenv()

db = SQLAlchemy()  
Base = automap_base()
def create_app() : 
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
   
    with app.app_context():
        Base.prepare(db.engine, reflect=True)
        global Products
        try:
            Products = Base.classes.products
        except Exception as e:
            print(f"Error: {e}")
            Products = None
    

    from app.routes.classifier_api import classification_bp
    from app.routes.intergration import integration_bp
    app.register_blueprint(classification_bp , url_prefix='/classification')
    app.register_blueprint(integration_bp , url_prefix='/integration')

    return app 