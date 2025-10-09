from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import db, Section
from forms import SectionForm

sections_bp = Blueprint('sections', __name__)


@sections_bp.route('/new', methods=['GET', 'POST'])
@login_required
def admin_section_new():
    form = SectionForm()
    if form.validate_on_submit():
        s = Section(title=form.title.data, description=form.description.data)
        db.session.add(s)
        db.session.commit()
        flash('Seção criada.', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/section_form.html', form=form, action='Criar')


@sections_bp.route('/<int:sid>/edit', methods=['GET', 'POST'])
@login_required
def admin_section_edit(sid):
    s = Section.query.get_or_404(sid)
    form = SectionForm(obj=s)
    if form.validate_on_submit():
        s.title = form.title.data
        s.description = form.description.data
        db.session.commit()
        flash('Seção atualizada.', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/section_form.html', form=form, action='Editar')


@sections_bp.route('/<int:sid>/delete', methods=['POST'])
@login_required
def admin_section_delete(sid):
    s = Section.query.get_or_404(sid)
    db.session.delete(s)
    db.session.commit()
    flash('Seção removida.', 'info')
    return redirect(url_for('admin.admin_dashboard'))
