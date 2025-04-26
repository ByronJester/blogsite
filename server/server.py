from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    blog = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set when a blog is created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Automatically update on modification

    def serialize(self):
        return {
            'id': self.id,
            'blog': self.blog,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Helper function to validate blog data
def validate_blog_data(data):
    if not data.get('blog'):
        return False, "Blog content is required."
    return True, None

# Fetch all blogs
@app.route("/api/blogs", methods=['GET'])
def return_blogs():
    try:
        blogs = Blog.query.all()
        return jsonify([b.serialize() for b in blogs])
    except Exception as e:
        print(f"Error fetching blogs: {e}")
        return jsonify({"error": "Failed to fetch blogs"}), 500

# Create a new blog
@app.route("/api/blogs", methods=['POST'])
def create_blog():
    data = request.get_json()

    # Validate the incoming request data
    is_valid, error_message = validate_blog_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    try:
        new_blog = Blog(
            blog=data['blog'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_blog)
        db.session.commit()
        return jsonify(new_blog.serialize()), 201
    except Exception as e:
        print(f"Error creating blog: {e}")
        return jsonify({"error": "Failed to create blog"}), 500

# Update an existing blog
@app.route("/api/blogs/<int:id>", methods=['PUT'])
def update_blog(id):
    data = request.get_json()

    # Validate the incoming request data
    is_valid, error_message = validate_blog_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    try:
        blog = Blog.query.get_or_404(id)
        blog.blog = data['blog']
        blog.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(blog.serialize())
    except Exception as e:
        print(f"Error updating blog: {e}")
        return jsonify({"error": "Failed to update blog"}), 500

# Delete an existing blog
@app.route("/api/blogs/<int:id>", methods=['DELETE'])
def delete_blog(id):
    try:
        blog = Blog.query.get_or_404(id)
        db.session.delete(blog)
        db.session.commit()
        return jsonify({"message": "Blog deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting blog: {e}")
        return jsonify({"error": "Failed to delete blog"}), 500

# Global error handler
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
