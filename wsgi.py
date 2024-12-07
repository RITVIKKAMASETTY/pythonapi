import sys
import os
from app import app as application

# Add the path to the current directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
