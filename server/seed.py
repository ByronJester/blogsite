from server.server import app, db, Blog
from datetime import datetime

def seed_db():
    with app.app_context():
        Blog.query.delete()  
        db.session.commit()  

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
