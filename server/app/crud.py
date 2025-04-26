from app.models import db, Blog
from sqlalchemy.exc import SQLAlchemyError

# Fetch all blogs
def get_all_blogs():
    try:
        return Blog.query.all()
    except SQLAlchemyError as e:
        raise e

# Create a new blog
def create_blog(blog_data):
    try:
        new_blog = Blog(blog=blog_data['blog'])
        db.session.add(new_blog)
        db.session.commit()
        return new_blog
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

# Update an existing blog
def update_blog(blog_id, blog_data):
    try:
        blog = Blog.query.get(blog_id)
        if blog:
            blog.blog = blog_data['blog']
            db.session.commit()
            return blog
        return None
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

# Delete a blog
def delete_blog(blog_id):
    try:
        blog = Blog.query.get(blog_id)
        if blog:
            db.session.delete(blog)
            db.session.commit()
            return blog
        return None
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
