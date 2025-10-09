# Optional: script to insert sample texts directly into DB (if you prefer)
from app import create_app
from models import db, Text, Section
app = create_app()
with app.app_context():
    db.create_all()
    s = Section.query.filter_by(title='Reflita comigo').first()
    if s:
        t = Text(title='Sentimentos na pandemia', subtitle='Uma memória', body='Este é um texto de exemplo.\n\nEscreva em *markdown* aqui.', published=True, section_id=s.id)
        db.session.add(t)
        db.session.commit()
        print('Texto exemplo criado.')
    else:
        print('Seção "Reflita comigo" não encontrada.')
