from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    texts = db.relationship('Text', backref='section', lazy=True, cascade='all, delete-orphan')

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    subtitle = db.Column(db.String(400))
    body = db.Column(db.Text)
    published = db.Column(db.Boolean, default=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
