from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import User, Section, Text
from forms import LoginForm
from models import db, Contact

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Bem-vindo ao painel.', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        flash('Credenciais inválidas.', 'danger')
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Saída efetuada.', 'info')
    return redirect(url_for('admin.admin_login'))


@admin_bp.route('/')
@login_required
def admin_dashboard():
    sections = Section.query.all()
    texts = Text.query.order_by(Text.created_at.desc()).limit(10).all()
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/dashboard.html', sections=sections, texts=texts, contacts=contacts)

@admin_bp.route('/contacts')
@login_required
def admin_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@admin_bp.route('/contacts/<int:cid>/responded', methods=['POST'])
@login_required
def admin_contact_responded(cid):
    contact = Contact.query.get_or_404(cid)
    contact.responded = True
    db.session.commit()
    flash(f'Marcado como respondido: {contact.name}', 'info')
    return redirect(url_for('admin.admin_contacts'))
