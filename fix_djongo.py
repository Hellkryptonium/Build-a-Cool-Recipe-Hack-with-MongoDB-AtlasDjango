import os
import traceback
from importlib import import_module

def patch_djongo_base():
    """Patch the _close method in djongo/base.py to avoid boolean check on database object"""
    try:
        # Find djongo installation path
        import djongo
        djongo_base_path = os.path.join(os.path.dirname(djongo.__file__), 'base.py')
        print(f"Found djongo base.py at: {djongo_base_path}")
        
        # Read the file
        with open(djongo_base_path, 'r') as f:
            content = f.read()
        
        # Create a backup of the original file
        with open(f"{djongo_base_path}.bak", 'w') as f:
            f.write(content)
        print(f"Created backup at: {djongo_base_path}.bak")
        
        # Find the _close method
        import re
        close_method_pattern = re.compile(r'def\s+_close\s*\(\s*self\s*\)\s*:(.*?)(?=\s+def|\s*$)', re.DOTALL)
        match = close_method_pattern.search(content)
        
        if not match:
            print("Could not find _close method in djongo/base.py")
            return False
        
        close_method = match.group(0)
        print(f"Found _close method: {close_method}")
        
        # Fix the method to avoid boolean check
        fixed_close_method = """def _close(self):
        # Fixed version that avoids bool() on Database object
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.client.close()"""
        
        # Replace the method
        patched_content = content.replace(close_method, fixed_close_method)
        
        # Write the patched file
        with open(djongo_base_path, 'w') as f:
            f.write(patched_content)
        
        print("Successfully patched djongo/base.py")
        return True
    
    except Exception as e:
        print(f"Error patching djongo/base.py: {e}")
        traceback.print_exc()
        return False

def patch_djongo_query():
    """Patch the _drop_column method in djongo/sql2mongo/query.py to use update_many instead of update"""
    try:
        # Find djongo installation path
        import djongo
        query_path = os.path.join(os.path.dirname(djongo.__file__), 'sql2mongo', 'query.py')
        print(f"Found djongo query.py at: {query_path}")
        
        # Read the file
        with open(query_path, 'r') as f:
            content = f.read()
        
        # Create a backup of the original file
        with open(f"{query_path}.bak", 'w') as f:
            f.write(content)
        print(f"Created backup at: {query_path}.bak")
        
        # Find the _drop_column method
        import re
        drop_column_pattern = re.compile(r'def\s+_drop_column\s*\(\s*self\s*\)\s*:(.*?)(?=\s+def|\s*$)', re.DOTALL)
        match = drop_column_pattern.search(content)
        
        if not match:
            print("Could not find _drop_column method in djongo/sql2mongo/query.py")
            return False
        
        drop_column_method = match.group(0)
        print(f"Found _drop_column method: {drop_column_method}")
        
        # Fix the method to use update_many instead of update
        fixed_drop_column_method = """def _drop_column(self):
        # Fixed version that uses update_many instead of update
        self.db[self.left_table].update_many(
            {},
            {
                '$unset': {self.field: ''},
            }
        )"""
        
        # Replace the method
        patched_content = content.replace(drop_column_method, fixed_drop_column_method)
        
        # Write the patched file
        with open(query_path, 'w') as f:
            f.write(patched_content)
        
        print("Successfully patched djongo/sql2mongo/query.py")
        return True
    
    except Exception as e:
        print(f"Error patching djongo/sql2mongo/query.py: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Patching djongo compatibility issues...")
    try:
        import djongo
        print(f"Found djongo installed at: {djongo.__file__}")
    except ImportError:
        print("ERROR: djongo is not installed. Please install it first.")
        exit(1)
    
    base_patched = patch_djongo_base()
    query_patched = patch_djongo_query()
    
    if base_patched and query_patched:
        print("Successfully patched all djongo compatibility issues!")
    elif base_patched:
        print("Patched djongo/base.py but failed to patch djongo/sql2mongo/query.py")
    elif query_patched:
        print("Patched djongo/sql2mongo/query.py but failed to patch djongo/base.py")
    else:
        print("Failed to patch any djongo files")
