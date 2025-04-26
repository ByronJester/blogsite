from flask import Blueprint, jsonify, request, redirect
from app.crud import get_all_blogs, create_blog, update_blog, delete_blog

blog_bp = Blueprint('blog_bp', __name__)

# Fetch all blogs
@blog_bp.route('/blogs', methods=['GET'])
def fetch_blogs():
    try:
        blogs = get_all_blogs()
        return jsonify([blog.serialize() for blog in blogs])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create a new blog
@blog_bp.route('/blogs', methods=['POST'])
def add_blog():
    data = request.get_json()
    if not data or not data.get('blog'):
        return jsonify({"error": "Blog content is required."}), 400
    
    try:
        new_blog = create_blog(data)
        return jsonify(new_blog.serialize()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update an existing blog
@blog_bp.route('/blogs/<int:id>', methods=['PUT'])
def modify_blog(id):
    data = request.get_json()
    if not data or not data.get('blog'):
        return jsonify({"error": "Blog content is required."}), 400

    try:
        updated_blog = update_blog(id, data)
        if updated_blog:
            return jsonify(updated_blog.serialize())
        return jsonify({"error": "Blog not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a blog
@blog_bp.route('/blogs/<int:id>', methods=['DELETE'])
def remove_blog(id):
    try:
        deleted_blog = delete_blog(id)
        if deleted_blog:
            return jsonify({"message": "Blog deleted successfully."}), 200
        return jsonify({"error": "Blog not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
