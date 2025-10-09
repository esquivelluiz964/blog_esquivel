import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from models import db, User, Section, Text
from apscheduler.schedulers.background import BackgroundScheduler
from models import WeeklyText

# Importa os blueprints
from routes.public_routes import public_bp
from routes.admin_routes import admin_bp
from routes.sections_routes import sections_bp
from routes.texts_routes import texts_bp


def seed_data():
    """Cria usuário admin e seções padrão se ainda não existirem."""
    if not User.query.filter_by(email=os.environ.get('ADMIN_EMAIL', 'admin@example.com')).first():
        admin = User(
            email=os.environ.get('ADMIN_EMAIL', 'admin@example.com'),
            password_hash=generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'ChangeMe123!'))
        )
        db.session.add(admin)

    sections = [
        ('Astrobiologia, ciência', 'Textos criados a partir da minha pesquisa acadêmica'),
        ('Católicos', 'Textos criados a partir da minha vida religiosa'),
        ('Escrita Perfeita', 'Divulgação dos meus e-book'),
        ('Marcas Memoraveis', 'Poemas criados ao longo da vida'),
        ('Reflita comigo', 'Textos aleatórios escritos sem pretensão nenhuma'),
    ]

    for sname, sdesc in sections:
        if not Section.query.filter_by(title=sname).first():
            s = Section(title=sname, description=sdesc)
            db.session.add(s)

    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///luis_site.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager(app)
    login_manager.login_view = 'admin.admin_login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        seed_data()

    # Registro dos blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(sections_bp, url_prefix='/admin/sections')
    app.register_blueprint(texts_bp, url_prefix='/admin/texts')

    # Rotas simples adicionais
    @app.route('/static_files/<path:filename>')
    def static_files(filename):
        return send_from_directory(os.path.join(app.root_path, 'static_files'), filename)

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=WeeklyText.rotate_weekly_text, trigger='interval', hours=12)
    scheduler.start()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
