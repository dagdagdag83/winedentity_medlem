import os
import datetime
import logging
import requests
import json
from flask import Flask, render_template, redirect, url_for, flash, session, request
from forms import RegistrationForm
from db import Database

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SESSION_SECRET_KEY', 'a_hard_to_guess_string')
app.config['RECAPTCHA_SITE_KEY'] = os.environ.get('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.environ.get('RECAPTCHA_SECRET_KEY')

# Initialize Database
db_manager = Database()

def verify_recaptcha(token):
    """Verifies the reCAPTCHA token with Google."""
    if not app.config['RECAPTCHA_SECRET_KEY']:
        logging.warning("RECAPTCHA_SECRET_KEY is not set. Skipping verification.")
        return True, 0.9  # Assume success for local development if not set

    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': app.config['RECAPTCHA_SECRET_KEY'],
                'response': token
            }
        )
        result = response.json()
        logging.debug(f"reCAPTCHA verification result: {result}")
        
        if result.get('success') and result.get('score', 0.0) >= 0.5:
            return True, result.get('score')
        else:
            return False, result.get('score')
    except Exception as e:
        logging.error(f"Error verifying reCAPTCHA: {e}")
        return False, 0.0

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    logging.debug(f"Request method: {request.method}")

    if request.method == 'POST':
        token = request.form.get('g-recaptcha-response')
        is_valid, score = verify_recaptcha(token)
        logging.debug(f"reCAPTCHA validation: is_valid={is_valid}, score={score}")

        if not is_valid:
            flash('reCAPTCHA verification failed. Please try again.', 'danger')
            return render_template('index.jinja2', form=form)

        if form.validate():
            logging.debug("Form validation successful.")
            try:
                member_number = db_manager.get_next_member_number()
                logging.debug(f"Next member number: {member_number}")

                member_data = {
                    'full_name': form.full_name.data,
                    'birth_date': datetime.datetime.combine(form.birth_date.data, datetime.time.min),
                    'address': form.address.data,
                    'postal_code': form.postal_code.data,
                    'country': form.country.data,
                    'email': form.email.data,
                    'phone': form.phone.data,
                    'company': form.company.data,
                    'membership_number': member_number,
                    'registration_date': datetime.datetime.now(datetime.timezone.utc)
                }
                logging.debug(f"Member data: {member_data}")
                db_manager.add_member(member_data)
                logging.debug("Member data added to the database.")

                session['membership_number'] = member_number
                session['full_name'] = form.full_name.data
                return redirect(url_for('success'))
            except Exception as e:
                logging.error(f"An error occurred: {e}", exc_info=True)
                flash(f'An error occurred: {e}', 'danger')
        else:
            logging.warning("Form validation failed.")
            logging.debug(f"Form errors: {form.errors}")

    # Pass countries to the template as a JSON object
    countries_json = json.dumps([{'value': value, 'text': text} for value, text in form.country.choices])
    
    return render_template('index.jinja2', form=form, countries_json=countries_json)

@app.route('/success')
def success():
    membership_number = session.get('membership_number', 'N/A')
    full_name = session.get('full_name', 'Member')
    return render_template('success.jinja2', full_name=full_name, membership_number=membership_number)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
