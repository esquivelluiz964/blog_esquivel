from flask import Blueprint, render_template, redirect, url_for, flash
from models import Section, Text
from forms import ContactForm
import markdown2

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def home():
    sections = Section.query.all()
    recent = Text.query.filter_by(published=True).order_by(Text.created_at.desc()).limit(5).all()
    return render_template('public/home.html', sections=sections, recent=recent)


@public_bp.route('/about')
def about():
    return render_template('public/about.html')


@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Mensagem enviada — obrigado!', 'success')
        return redirect(url_for('public.contact'))
    return render_template('public/contact.html', form=form)


@public_bp.route('/section/<int:section_id>')
def section_view(section_id):
    section = Section.query.get_or_404(section_id)
    texts = Text.query.filter_by(section_id=section.id, published=True).order_by(Text.created_at.desc()).all()
    return render_template('public/section.html', section=section, texts=texts)


@public_bp.route('/text/<int:text_id>')
def text_view(text_id):
    text = Text.query.get_or_404(text_id)
    html = markdown2.markdown(text.body or '')
    return render_template('public/text.html', text=text, html=html)
