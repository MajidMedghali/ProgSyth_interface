from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin depuis le frontend React

from backend import routes
