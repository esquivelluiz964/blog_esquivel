from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
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

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Contact {self.name} ({'Respondido' if self.responded else 'Novo'})>"

class WeeklyText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_id = db.Column(db.Integer, db.ForeignKey('text.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)

    text = db.relationship('Text', backref='weekly_entry', lazy=True)

    @staticmethod
    def rotate_weekly_text():
        """Troca automaticamente o texto da semana se já passou 7 dias."""
        current = WeeklyText.query.filter_by(active=True).first()
        if current and current.end_date and current.end_date < datetime.utcnow():
            current.active = False
            db.session.commit()
            # Busca o próximo texto publicado mais recente
            next_text = Text.query.filter_by(published=True).order_by(Text.created_at.desc()).first()
            if next_text:
                new_week = WeeklyText(
                    text_id=next_text.id,
                    start_date=datetime.utcnow(),
                    end_date=datetime.utcnow() + timedelta(days=7),
                    active=True
                )
                db.session.add(new_week)
                db.session.commit()
