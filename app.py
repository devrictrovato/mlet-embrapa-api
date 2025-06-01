from flask import Flask, render_template
from flasgger import Swagger
from flask_caching import Cache

from routes.production import production_routes
from routes.processing import processing_routes
from routes.commercialization import commercialization_routes
from routes.importation import importation_routes
from routes.exportation import exportation_routes

app = Flask(__name__)

cache = Cache()
app.config['CACHE_TYPE'] = 'SimpleCache'  # Pode ser Redis, Memcached, etc.
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache.init_app(app)

Swagger(app)

@app.route('/')
@cache.cached()
def home():
    return render_template('index.html')

app.register_blueprint(production_routes)
app.register_blueprint(processing_routes)
app.register_blueprint(commercialization_routes)
app.register_blueprint(importation_routes)
app.register_blueprint(exportation_routes)

if __name__ == '__main__':
    app.run(debug=True)