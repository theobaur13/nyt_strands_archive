from app import app, db
from app.models import Strand, Letters, Words, WordLetters, User
from datetime import datetime

def load_db():
    users = {
        "admin_1": {
            "username": "admin",
            "password": "password"
        }
    }

    with app.app_context():
        db.drop_all()
        db.create_all()

        for user in users:
            new_user = User(
                username=users[user]["username"],
                hashed_password=users[user]["password"]
            )
            db.session.add(new_user)

        db.session.commit()

if __name__ == "__main__":
    load_db()