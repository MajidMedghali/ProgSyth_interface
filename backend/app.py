from flask import Flask
from routes import routes
import argparse
#from ProgSynth.examples.pbe import dsl_loader
# from synth.pbe.solvers import CutoffPBESolver
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
