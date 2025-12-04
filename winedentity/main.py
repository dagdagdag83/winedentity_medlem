import datetime
import logging
import json
import os
from flask import render_template, redirect, url_for, flash, session, request
from . import app, db_manager
from .forms import RegistrationForm
from .utils import verify_recaptcha
from .countries import COUNTRIES

def home_view():
    return render_template('home.jinja2')

def register_view():
    form = RegistrationForm()
    logging.debug(f"Request method: {request.method}")

    if request.method == 'POST':
        if os.environ.get('ENV') != 'local':
            token = request.form.get('g-recaptcha-response')
            is_valid, score = verify_recaptcha(token, app.config['RECAPTCHA_SECRET_KEY'])
            logging.debug(f"reCAPTCHA validation: is_valid={is_valid}, score={score}")

<<<<<<< HEAD:app.py
        if not is_valid:
            flash('reCAPTCHA verification failed. Please try again.', 'danger')
            return render_template('reg.jinja2', form=form)
=======
            if not is_valid:
                flash('reCAPTCHA verification failed. Please try again.', 'danger')
                return render_template('index.jinja2', form=form)
>>>>>>> af26ce4a1ad4c3b7e3335a33b728bb8df7324fda:winedentity/main.py

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
    countries_json = json.dumps([{'value': value, 'text': text} for value, text in COUNTRIES])
    
<<<<<<< HEAD:app.py
    return render_template('reg.jinja2', form=form, countries_json=countries_json)
=======
    return render_template('index.jinja2', form=form, countries_json=countries_json, env=os.environ.get('ENV'))
>>>>>>> af26ce4a1ad4c3b7e3335a33b728bb8df7324fda:winedentity/main.py

@app.route('/success')
def success():
    membership_number = session.get('membership_number', 'N/A')
    full_name = session.get('full_name', 'Member')
    return render_template('success.jinja2', full_name=full_name, membership_number=membership_number)
<<<<<<< HEAD:app.py

# Routing Logic
if os.environ.get('ENV') == 'LOCAL':
    app.add_url_rule('/', view_func=home_view)
    app.add_url_rule('/reg', view_func=register_view, methods=['GET', 'POST'])
else:
    @app.route('/', methods=['GET', 'POST'])
    def dispatch():
        host = request.host.split(':')[0]
        logging.debug(f"Dispatching for host: {host}")
        
        if host == 'winedentity.org':
            return home_view()
        elif host == 'reg.winedentity.org':
            return register_view()
        else:
            return "Not Found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
=======
>>>>>>> af26ce4a1ad4c3b7e3335a33b728bb8df7324fda:winedentity/main.py
