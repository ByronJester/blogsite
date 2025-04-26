# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from app.models import db  # Initialize db object here
from app.routes.blog_routes import blog_bp

def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Enable CORS for the React frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Load the database URL from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database and migration objects
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Migrate
    
    # Register the blog routes with the app
    app.register_blueprint(blog_bp, url_prefix="/api")

    # Debug: Print all registered routes
    print("\nRegistered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    return app
