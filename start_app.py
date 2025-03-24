# Simple starter script that doesn't import any other modules yet
import os
import sys
from datetime import datetime

print(f"===== Starter Script at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory:")
for file in sorted(os.listdir()):
    print(f"  - {file}")

try:
    print("\nTrying to import app.py...")
    import app
    print("Successfully imported app")
    
    if hasattr(app, 'app'):
        print("Running the Flask app...")
        app.app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860)))
    else:
        print("No 'app' variable found in app.py")
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc() 