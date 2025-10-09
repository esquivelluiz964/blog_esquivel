from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])

class SectionForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = StringField('Descrição', validators=[Length(max=500)])

class TextForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=300)])
    subtitle = StringField('Subtítulo', validators=[Length(max=400)])
    section = SelectField('Seção', coerce=int)
    body = TextAreaField('Corpo (markdown)', validators=[DataRequired()])
    published = BooleanField('Publicado')

class ContactForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Mensagem', validators=[DataRequired(), Length(max=2000)])
