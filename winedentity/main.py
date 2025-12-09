import datetime
import logging
import json
import os
from flask import render_template, redirect, url_for, flash, session, request
from . import app, db_manager
from .forms import RegistrationForm
from .utils import verify_recaptcha
from .countries import COUNTRIES

@app.context_processor
def inject_env():
    return dict(env=os.environ.get('ENV'))

def home_view():
    return render_template('home.jinja2', env=os.environ.get('ENV'))

def register_view():
    form = RegistrationForm()
    logging.debug(f"Request method: {request.method}")

    if request.method == 'POST':
        is_valid = True # Default to True for local dev
        if os.environ.get('ENV') != 'local':
            token = request.form.get('g-recaptcha-response')
            is_valid, score = verify_recaptcha(token, app.config['RECAPTCHA_SECRET_KEY'])
            logging.debug(f"reCAPTCHA validation: is_valid={is_valid}, score={score}")

        if not is_valid:
            flash('reCAPTCHA verification failed. Please try again.', 'danger')
            return render_template('reg.jinja2', form=form)

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
    
    return render_template('reg.jinja2', form=form, countries_json=countries_json, env=os.environ.get('ENV'))

@app.route('/success')
def success():
    membership_number = session.get('membership_number', 'N/A')
    full_name = session.get('full_name', 'Member')
    return render_template('success.jinja2', full_name=full_name, membership_number=membership_number)

# Routing Logic
if os.environ.get('ENV') == 'local':
    app.add_url_rule('/', view_func=home_view)
    app.add_url_rule('/reg', view_func=register_view, methods=['GET', 'POST'])
else:
    @app.route('/', methods=['GET', 'POST'])
    def dispatch():
        host = request.host.split(':')[0]
        logging.debug(f"Dispatching for host: {host}")
        
        if host == 'winedentity.org' or host == 'www.winedentity.org':
            return home_view()
        elif host == 'reg.winedentity.org':
            return register_view()
        else:
            return "Not Found", 404
