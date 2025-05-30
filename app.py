from flask import Flask, jsonify
from production import production_routes
from processing import processing_routes
from commercialization import commercialization_routes
from importation import importation_routes
from exportation import exportation_routes

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask!'

app.register_blueprint(production_routes)
app.register_blueprint(processing_routes)
app.register_blueprint(commercialization_routes)
app.register_blueprint(importation_routes)
app.register_blueprint(exportation_routes)

if __name__ == '__main__':
    app.run(debug=True)