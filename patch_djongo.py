import sys
import os
from pymongo.database import Database

# Get the path to the djongo base.py file
djongo_base_path = os.path.join(sys.prefix, 'Lib', 'site-packages', 'djongo', 'base.py')

# Read the current file
with open(djongo_base_path, 'r') as f:
    content = f.read()

# Define the patch for the _close method
old_close = '''    def _close(self):
        if self.connection:
            self.connection.client.close()'''

new_close = '''    def _close(self):
        # Fixed version that avoids bool() on Database object
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.client.close()'''

# Apply the patch
patched_content = content.replace(old_close, new_close)

# Write the patched file
with open(djongo_base_path, 'w') as f:
    f.write(patched_content)

print("Patched djongo base.py successfully!")

# Now fix the SQL2Mongo query.py file for update() method
djongo_query_path = os.path.join(sys.prefix, 'Lib', 'site-packages', 'djongo', 'sql2mongo', 'query.py')

# Read the query.py file
with open(djongo_query_path, 'r') as f:
    query_content = f.read()

# Define the patch for the _drop_column method
old_drop_column = '''    def _drop_column(self):
        self.db[self.left_table].update(
            {},
            {
                '$unset': {self.field: ''},
            },
            multi=True
        )'''

new_drop_column = '''    def _drop_column(self):
        # Fixed version that uses update_many instead of update
        self.db[self.left_table].update_many(
            {},
            {
                '$unset': {self.field: ''},
            }
        )'''

# Apply the patch
patched_query_content = query_content.replace(old_drop_column, new_drop_column)

# Write the patched file
with open(djongo_query_path, 'w') as f:
    f.write(patched_query_content)

print("Patched djongo sql2mongo/query.py successfully!")