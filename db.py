import os
from google.cloud import datastore

# Initialize Datastore DB
# The client will automatically use the credentials from the environment variable.
db = datastore.Client(project="winedentity", database="medlemsregister")

class Database:
    def __init__(self):
        self.client = db

    def get_next_member_number(self):
        """
        Gets the next member number from Datastore atomically using a transaction.
        """
        with self.client.transaction() as transaction:
            # Create a key for the counter entity
            counter_key = self.client.key('counters', 'member_counter')
            
            # Get the counter entity inside the transaction
            counter = self.client.get(counter_key)

            if not counter:
                # Initialize counter if it doesn't exist
                next_number = 1001
                counter = datastore.Entity(key=counter_key)
                counter['current_number'] = next_number
            else:
                # Increment the existing counter
                current_number = counter.get('current_number', 1000)
                next_number = current_number + 1
                counter['current_number'] = next_number

            # Save the updated counter
            transaction.put(counter)
            
            return next_number

    def add_member(self, member_data):
        """
        Adds a new member entity to Datastore.
        """
        # Create a new key for the 'members' kind.
        # Datastore will automatically generate a unique ID.
        member_key = self.client.key('members')
        
        # Create a new entity
        member_entity = datastore.Entity(key=member_key)
        
        # Update the entity with the member data
        member_entity.update(member_data)
        
        # Save the entity to Datastore
        self.client.put(member_entity)
