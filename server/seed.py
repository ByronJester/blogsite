from server import app, db, Blog
from datetime import datetime

def seed_db():
    with app.app_context():
        # Clear the existing data before seeding new blogs
        Blog.query.delete()  # This will delete all existing records in the 'blogs' table
        db.session.commit()  # Commit the changes to the database

        # Now add the new blogs
        blogs = [
            Blog(blog="First Blog", created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            Blog(blog="Second Blog", created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            Blog(blog="Third Blog", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        ]
        db.session.bulk_save_objects(blogs)
        db.session.commit()

        print("Database seeded with initial blogs!")

if __name__ == '__main__':
    seed_db()
