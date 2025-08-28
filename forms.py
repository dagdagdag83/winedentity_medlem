from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    full_name = StringField('Fullt Navn', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    postal_code = StringField('Postnummer', validators=[DataRequired(), Length(min=4, max=10)])
    country = SelectField('Land', choices=[('NO', 'Norge'), ('SE', 'Sverige'), ('DK', 'Danmark'), ('FI', 'Finland'), ('GB', 'Storbritannia'), ('US', 'USA')], validators=[DataRequired()])
    email = StringField('E-post', validators=[DataRequired()])
    phone = StringField('Telefon', validators=[DataRequired()])
    company = StringField('Firma (valgfritt)')
    confirm = BooleanField('Jeg bekrefter at opplysningene gitt er riktige.', validators=[DataRequired()])
    submit = SubmitField('Registrer deg')
