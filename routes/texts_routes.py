from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import db, Text, Section
from forms import TextForm

texts_bp = Blueprint('texts', __name__)


@texts_bp.route('/new', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/text_form.html', form=form, action='Criar')


@texts_bp.route('/<int:tid>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/text_form.html', form=form, action='Editar')


@texts_bp.route('/<int:tid>/delete', methods=['POST'])
@login_required
def admin_text_delete(tid):
    t = Text.query.get_or_404(tid)
    db.session.delete(t)
    db.session.commit()
    flash('Texto removido.', 'info')
    return redirect(url_for('admin.admin_dashboard'))
