class MockDatabase:
    """
    A mock database class for local development and testing.
    This class mimics the interface of the real Database class but uses
    an in-memory store instead of Google Cloud Datastore.
    """
    def __init__(self):
        """Initializes the mock database with an in-memory store."""
        self._members = []
        self._counter = 1000  # Start from 1000, so first member number is 1001

    def get_next_member_number(self):
        """
        Gets the next member number sequentially.
        This is a simplified, non-atomic version for mock purposes.
        """
        self._counter += 1
        return self._counter

    def add_member(self, member_data):
        """
        Adds a new member to the in-memory list.
        """
        self._members.append(member_data)
        print(f"MockDB: Added member {member_data.get('full_name')}. Total members: {len(self._members)}")

    def get_all_members(self):
        """A helper method to retrieve all members for testing."""
        return self._members
