from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_babel import lazy_gettext as _l

class RegistrationForm(FlaskForm):
    full_name = StringField(_l('Full Name'), validators=[DataRequired()])
    address = StringField(_l('Address'), validators=[DataRequired()])
    postal_code = StringField(_l('Postal Code'), validators=[DataRequired(), Length(min=4, max=10)])
    country = SelectField(_l('Country'), choices=[('NO', 'Norway'), ('SE', 'Sweden'), ('DK', 'Denmark'), ('FI', 'Finland'), ('GB', 'United Kingdom'), ('US', 'United States')], validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    phone = StringField(_l('Phone'), validators=[DataRequired()])
    company = StringField(_l('Company (optional)'))
    submit = SubmitField(_l('Register'))
