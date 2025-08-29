from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired, Length
from .countries import COUNTRIES

class RegistrationForm(FlaskForm):
    full_name = StringField('Fullt Navn', validators=[DataRequired()])
    birth_date = DateField('Fødselsdato', format='%d/%m/%Y', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    postal_code = StringField('Postnummer', validators=[DataRequired(), Length(min=4, max=10)])
    country = SelectField('Land', choices=COUNTRIES, default='NO', validators=[DataRequired()])

    email = StringField('E-post', validators=[DataRequired()])
    phone = StringField('Telefon', validators=[DataRequired()])
    company = StringField('Firma (valgfritt)')
    confirm = BooleanField('Jeg bekrefter at opplysningene gitt er riktige.', validators=[DataRequired()])
    submit = SubmitField('Registrer deg')
