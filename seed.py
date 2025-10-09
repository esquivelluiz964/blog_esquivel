from app import create_app
from models import db, User, Section
from werkzeug.security import generate_password_hash
import os

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email=os.environ.get('ADMIN_EMAIL','admin@gmail.com')).first():
        admin = User(email=os.environ.get('ADMIN_EMAIL','admin@gmail.com'),
                     password_hash=generate_password_hash(os.environ.get('ADMIN_PASSWORD','123456')))
        db.session.add(admin)
    sections = [
        ('Astrobiologia, ciência', 'Textos criados a partir da minha pesquisa acadêmica'),
        ('Católicos', 'Textos criados a partir da minha vida religiosa'),
        ('Escrita Perfeita', 'Divulgação dos meus e-book'),
        ('Marcas Memoraveis', 'Poemas criados ao longo da vida'),
        ('Reflita comigo', 'Textos aleatórios escritos sem pretensão nenhuma'),
    ]
    for title,desc in sections:
        if not Section.query.filter_by(title=title).first():
            db.session.add(Section(title=title, description=desc))
    db.session.commit()
    print('Seed concluído.')
