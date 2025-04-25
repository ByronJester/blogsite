from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Create Flask app and configure CORS and DB
app = Flask(__name__)

# Allow requests only from localhost:3000
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# PostgreSQL URI (Make sure it's correct)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://byronjestermanalo:49TCwszWtB1tuZK67FmireVGKQrxudse@dpg-d05o29ili9vc7390lji0-a.singapore-postgres.render.com/blogsite_un1j'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Blog Model with created_at and updated_at
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

# Fetch all blogs
@app.route("/api/blogs", methods=['GET'])
def return_blogs():
    try:
        blogs = Blog.query.all()
        return jsonify([b.serialize() for b in blogs])
    except Exception as e:
        print(f"Error fetching blogs: {e}")
        return jsonify({"error": str(e)}), 500

# Create a new blog
@app.route("/api/blogs", methods=['POST'])
def create_blog():
    try:
        data = request.get_json()
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
        return jsonify({"error": str(e)}), 500

# Update an existing blog
@app.route("/api/blogs/<int:id>", methods=['PUT'])
def update_blog(id):
    try:
        data = request.get_json()
        blog = Blog.query.get_or_404(id)
        blog.blog = data['blog']
        blog.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(blog.serialize())
    except Exception as e:
        print(f"Error updating blog: {e}")
        return jsonify({"error": str(e)}), 500

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
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
