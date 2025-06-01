from flask import Flask, render_template
from flasgger import Swagger
from flask_caching import Cache
from flask_jwt_extended import JWTManager

from routes.production import production_routes
from routes.processing import processing_routes
from routes.commercialization import commercialization_routes
from routes.importation import importation_routes
from routes.exportation import exportation_routes

from db.database import db
from auth.authentication import auth_routes

app = Flask(__name__)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = '6fe4fbe5c833d787fb97c2211cfa6f8eef0437ebf4052c7e9eff6de008205443'
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# Inicializações
db.init_app(app)
jwt = JWTManager(app)
cache = Cache(app)
docs = Swagger(app, template={
    'swagger': '2.0',
    'info': {
        'title': 'Vitibrasil API',
        'description': 'API com autenticação JWT',
        'version': '1.0'
    },
    'securityDefinitions': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Insira o token JWT no formato: Bearer <seu_token>'
        }
    }
})

# Criação das tabelas
@app.before_request
def create_tables():
    db.create_all()

# Página inicial
@app.route('/')
@cache.cached()
def home():
    return render_template('index.html')

# Registro das rotas
app.register_blueprint(auth_routes)
app.register_blueprint(production_routes)
app.register_blueprint(processing_routes)
app.register_blueprint(commercialization_routes)
app.register_blueprint(importation_routes)
app.register_blueprint(exportation_routes)

if __name__ == '__main__':
    app.run(debug=True)
