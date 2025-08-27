import os
import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from forms import RegistrationForm
from db import Database

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_hard_to_guess_string')

# Initialize Database
db_manager = Database()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            member_number = db_manager.get_next_member_number()

            member_data = {
                'full_name': form.full_name.data,
                'email': form.email.data,
                'membership_number': member_number,
                'registration_date': datetime.datetime.now(datetime.timezone.utc)
            }
            db_manager.add_member(member_data)

            session['membership_number'] = member_number
            session['full_name'] = form.full_name.data
            return redirect(url_for('success'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
    return render_template('index.html', form=form)

@app.route('/success')
def success():
    membership_number = session.get('membership_number', 'N/A')
    full_name = session.get('full_name', 'Member')
    return render_template('success.html', full_name=full_name, membership_number=membership_number)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
