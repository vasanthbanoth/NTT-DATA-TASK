import os
import sys

# Add the parent directory to sys.path so we can import app.py from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel needs 'app' (the Flask object) to be available
# It acts as the WSGI application
