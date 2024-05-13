from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Strand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    theme = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Strand('{self.date}', '{self.theme}')"
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime("%Y-%m-%d"),
            "theme": self.theme
        }

class Letters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(1), nullable=False)
    strand_id = db.Column(db.Integer, db.ForeignKey("strand.id"), nullable=False)
    strand = db.relationship("Strand", backref=db.backref("letters", lazy=True))

    def __repr__(self):
        return f"Letter('{self.letter}')"
    
    def to_dict(self):
        return {
            "id": self.id,
            "index": self.index,
            "letter": self.letter,
            "strand_id": self.strand_id
        }

class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(120), nullable=False)
    spanagram = db.Column(db.Boolean, nullable=False, default=False)
    strand_id = db.Column(db.Integer, db.ForeignKey("strand.id"), nullable=False)
    strand = db.relationship("Strand", backref=db.backref("words", lazy=True))

class WordLetters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=False)
    word = db.relationship("Words", backref=db.backref("word_letters", lazy=True))
    letter_id = db.Column(db.Integer, db.ForeignKey("letters.id"), nullable=False)
    letter = db.relationship("Letters", backref=db.backref("word_letters", lazy=True))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    _hashed_password = db.Column('hashed_password', db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}')"

    @property
    def hashed_password(self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, password):
        self._hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._hashed_password, password)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))