import os
import datetime
import logging
from flask import Flask, render_template, redirect, url_for, flash, session, request
from forms import RegistrationForm
from db import Database

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SESSION_SECRET_KEY', 'a_hard_to_guess_string')

# Initialize Database
db_manager = Database()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    logging.debug(f"Request method: {request.method}")
    if form.validate_on_submit():
        logging.debug("Form validation successful.")
        try:
            member_number = db_manager.get_next_member_number()
            logging.debug(f"Next member number: {member_number}")

            member_data = {
                'full_name': form.full_name.data,
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
    elif request.method == 'POST':
        logging.warning("Form validation failed.")
        logging.debug(f"Form errors: {form.errors}")
    return render_template('index.jinja2', form=form)

@app.route('/success')
def success():
    membership_number = session.get('membership_number', 'N/A')
    full_name = session.get('full_name', 'Member')
    return render_template('success.jinja2', full_name=full_name, membership_number=membership_number)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
