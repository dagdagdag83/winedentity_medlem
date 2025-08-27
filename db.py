import datetime

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

class Database:
    def __init__(self):
        self.db = db

    @transactional
    def _get_next_member_number_atomic(self, transaction):
        """
        Gets the next member number from Firestore atomically using a transaction.
        """
        counter_ref = self.db.collection('counters').document('member_counter')
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

    def get_next_member_number(self):
        transaction = self.db.transaction()
        return self._get_next_member_number_atomic(transaction)

    def add_member(self, member_data):
        self.db.collection('members').add(member_data)
