import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, SectionForm, TextForm, ContactForm
from models import db, User, Section, Text
from werkzeug.security import generate_password_hash, check_password_hash
import markdown2


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
    login_manager.login_view = 'admin_login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Inicializa DB e faz seed apenas uma vez no startup
    with app.app_context():
        db.create_all()
        seed_data()

    # ----------------------
    # ROTAS PÚBLICAS
    # ----------------------
    @app.route('/')
    def home():
        sections = Section.query.all()
        recent = Text.query.filter_by(published=True).order_by(Text.created_at.desc()).limit(5).all()
        return render_template('public/home.html', sections=sections, recent=recent)

    @app.route('/about')
    def about():
        return render_template('public/about.html')

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            flash('Mensagem enviada — obrigado! (isso é um protótipo; configure SMTP no futuro)', 'success')
            return redirect(url_for('contact'))
        return render_template('public/contact.html', form=form)

    @app.route('/section/<int:section_id>')
    def section_view(section_id):
        section = Section.query.get_or_404(section_id)
        texts = Text.query.filter_by(section_id=section.id, published=True).order_by(Text.created_at.desc()).all()
        return render_template('public/section.html', section=section, texts=texts)

    @app.route('/text/<int:text_id>')
    def text_view(text_id):
        text = Text.query.get_or_404(text_id)
        html = markdown2.markdown(text.body or '')
        return render_template('public/text.html', text=text, html=html)

    # ----------------------
    # ROTAS ADMIN
    # ----------------------
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Bem-vindo ao painel.', 'success')
                return redirect(url_for('admin_dashboard'))
            flash('Credenciais inválidas.', 'danger')
        return render_template('admin/login.html', form=form)

    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        logout_user()
        flash('Saída efetuada.', 'info')
        return redirect(url_for('admin_login'))

    @app.route('/admin/')
    @login_required
    def admin_dashboard():
        sections = Section.query.all()
        texts = Text.query.order_by(Text.created_at.desc()).limit(10).all()
        return render_template('admin/dashboard.html', sections=sections, texts=texts)

    # ----------------------
    # CRUD DE SEÇÕES
    # ----------------------
    @app.route('/admin/sections/new', methods=['GET', 'POST'])
    @login_required
    def admin_section_new():
        form = SectionForm()
        if form.validate_on_submit():
            s = Section(title=form.title.data, description=form.description.data)
            db.session.add(s)
            db.session.commit()
            flash('Seção criada.', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/section_form.html', form=form, action='Criar')

    @app.route('/admin/sections/<int:sid>/edit', methods=['GET', 'POST'])
    @login_required
    def admin_section_edit(sid):
        s = Section.query.get_or_404(sid)
        form = SectionForm(obj=s)
        if form.validate_on_submit():
            s.title = form.title.data
            s.description = form.description.data
            db.session.commit()
            flash('Seção atualizada.', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/section_form.html', form=form, action='Editar')

    @app.route('/admin/sections/<int:sid>/delete', methods=['POST'])
    @login_required
    def admin_section_delete(sid):
        s = Section.query.get_or_404(sid)
        db.session.delete(s)
        db.session.commit()
        flash('Seção removida.', 'info')
        return redirect(url_for('admin_dashboard'))

    # ----------------------
    # CRUD DE TEXTOS
    # ----------------------
    @app.route('/admin/texts/new', methods=['GET', 'POST'])
    @login_required
    def admin_text_new():
        form = TextForm()
        form.section.choices = [(s.id, s.title) for s in Section.query.order_by(Section.title).all()]
        if form.validate_on_submit():
            t = Text(
                title=form.title.data,
                subtitle=form.subtitle.data,
                body=form.body.data,
                section_id=form.section.data,
                published=form.published.data
            )
            db.session.add(t)
            db.session.commit()
            flash('Texto criado.', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/text_form.html', form=form, action='Criar')

    @app.route('/admin/texts/<int:tid>/edit', methods=['GET', 'POST'])
    @login_required
    def admin_text_edit(tid):
        t = Text.query.get_or_404(tid)
        form = TextForm(obj=t)
        form.section.choices = [(s.id, s.title) for s in Section.query.order_by(Section.title).all()]
        if form.validate_on_submit():
            t.title = form.title.data
            t.subtitle = form.subtitle.data
            t.body = form.body.data
            t.section_id = form.section.data
            t.published = form.published.data
            db.session.commit()
            flash('Texto atualizado.', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/text_form.html', form=form, action='Editar')

    @app.route('/admin/texts/<int:tid>/delete', methods=['POST'])
    @login_required
    def admin_text_delete(tid):
        t = Text.query.get_or_404(tid)
        db.session.delete(t)
        db.session.commit()
        flash('Texto removido.', 'info')
        return redirect(url_for('admin_dashboard'))

    # ----------------------
    # DOWNLOADS / EBOOKS
    # ----------------------
    @app.route('/static_files/<path:filename>')
    def static_files(filename):
        return send_from_directory(os.path.join(app.root_path, 'static_files'), filename)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
