from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    full_name = StringField('Fullt Navn', validators=[DataRequired()])
    birth_date = DateField('Fødselsdato', format='%d/%m/%Y', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    postal_code = StringField('Postnummer', validators=[DataRequired(), Length(min=4, max=10)])
    
    # Define countries as a simple list of tuples
    countries = [
        ('NO', 'Norge'), ('DK', 'Danmark'), ('FI', 'Finland'), ('IS', 'Island'), ('SE', 'Sverige'),
        ('AL', 'Albania'), ('BD', 'Bangladesh'), ('BE', 'Belgia'), ('BA', 'Bosnia-Hercegovina'),
        ('BR', 'Brasil'), ('BG', 'Bulgaria'), ('CA', 'Canada'), ('EE', 'Estland'), ('FR', 'Frankrike'),
        ('GR', 'Hellas'), ('BY', 'Hviterussland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IE', 'Irland'),
        ('IT', 'Italia'), ('JP', 'Japan'), ('KZ', 'Kasakhstan'), ('CN', 'Kina'), ('HR', 'Kroatia'),
        ('CY', 'Kypros'), ('LV', 'Latvia'), ('LT', 'Litauen'), ('LU', 'Luxembourg'), ('MX', 'Mexico'),
        ('MD', 'Moldova'), ('ME', 'Montenegro'), ('NL', 'Nederland'), ('NG', 'Nigeria'),
        ('MK', 'Nord-Makedonia'), ('PK', 'Pakistan'), ('PL', 'Polen'), ('PT', 'Portugal'),
        ('RO', 'Romania'), ('RU', 'Russland'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'),
        ('ES', 'Spania'), ('GB', 'Storbritannia'), ('CH', 'Sveits'), ('ZA', 'Sør-Afrika'),
        ('CZ', 'Tsjekkia'), ('TR', 'Tyrkia'), ('DE', 'Tyskland'), ('UA', 'Ukraina'), ('HU', 'Ungarn'),
        ('US', 'USA'), ('AT', 'Østerrike'), ('XX', 'Annet')
    ]
    country = SelectField('Land', choices=countries, default='NO', validators=[DataRequired()])
    
    email = StringField('E-post', validators=[DataRequired()])
    phone = StringField('Telefon', validators=[DataRequired()])
    company = StringField('Firma (valgfritt)')
    confirm = BooleanField('Jeg bekrefter at opplysningene gitt er riktige.', validators=[DataRequired()])
    submit = SubmitField('Registrer deg')
