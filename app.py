import os
import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from forms import RegistrationForm

# A mock Firestore client for local testing without credentials
class MockFirestore:
    def __init__(self):
        self.collections = {}
        self._transaction = None

    def collection(self, name):
        if name not in self.collections:
            self.collections[name] = MockCollection(name, self)
        return self.collections[name]

    def transaction(self):
        self._transaction = MockTransaction(self)
        return self._transaction

class MockTransaction:
    def __init__(self, db):
        self.db = db
        self._reads = []
        self._writes = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            for write in self._writes:
                write()

    def get(self, ref):
        self._reads.append(ref)
        return ref.get()

    def set(self, ref, data):
        self._writes.append(lambda: ref.set(data))

    def update(self, ref, data):
        self._writes.append(lambda: ref.update(data))

class MockCollection:
    def __init__(self, name, db):
        self.name = name
        self.documents = {}
        self.db = db

    def document(self, name):
        if name not in self.documents:
            self.documents[name] = MockDocument(name, self)
        return self.documents[name]

    def add(self, data):
        doc_id = str(len(self.documents) + 1)
        self.documents[doc_id] = MockDocument(doc_id, self)
        self.documents[doc_id].set(data)
        return datetime.datetime.now(datetime.timezone.utc), self.documents[doc_id]

class MockDocument:
    def __init__(self, name, collection):
        self.name = name
        self.collection = collection
        self._data = {}
        self.exists = False

    def get(self):
        return self

    def set(self, data):
        self._data = data
        self.exists = True

    def update(self, data):
        self._data.update(data)

    def to_dict(self):
        return self._data

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_hard_to_guess_string')

# Initialize Firestore DB
try:
    from google.cloud import firestore
    db = firestore.Client()
    # Add a transactional decorator for the real Firestore client
    transactional = firestore.transactional
except Exception as e:
    print("Could not connect to Firestore, using a mock client for local testing.")
    print(e)
    db = MockFirestore()
    # A mock transactional decorator
    def transactional(to_wrap):
        def wrapper(transaction, *args, **kwargs):
            return to_wrap(transaction, *args, **kwargs)
        return wrapper

@transactional
def get_next_member_number_atomic(transaction):
    """
    Gets the next member number from Firestore atomically using a transaction.
    """
    counter_ref = db.collection('counters').document('member_counter')
    counter_snapshot = transaction.get(counter_ref)

    if not counter_snapshot.exists:
        # Initialize counter if it doesn't exist
        next_number = 1001
        transaction.set(counter_ref, {'current_number': next_number})
    else:
        current_number = counter_snapshot.to_dict().get('current_number', 1000)
        next_number = current_number + 1
        transaction.update(counter_ref, {'current_number': next_number})

    return next_number

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            transaction = db.transaction()
            member_number = get_next_member_number_atomic(transaction)

            member_data = {
                'full_name': form.full_name.data,
                'email': form.email.data,
                'membership_number': member_number,
                'registration_date': datetime.datetime.now(datetime.timezone.utc)
            }
            db.collection('members').add(member_data)

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
