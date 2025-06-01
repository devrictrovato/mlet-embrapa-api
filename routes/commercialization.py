import pandas as pd
import datetime

from flask import Blueprint, jsonify, request
from flasgger import swag_from

from web.scrapping import get_data

from flask_jwt_extended import verify_jwt_in_request

commercialization_routes = Blueprint('commercialization', __name__)

# Aplica verificação JWT a todas as rotas do blueprint
@commercialization_routes.before_request
def require_jwt():
    verify_jwt_in_request()

@commercialization_routes.route('/commercialization')
@swag_from({
    'tags': ['Vitivinicultura'],
    'summary': 'Retorna dados de comercialização de produtos vitivinícolas por ano.',
    'description': (
        'Esta rota requer autenticação JWT.\n'
        'Busca dados de comercialização usando o ano informado como parâmetro. '
        'Se a função `get_data` não retornar dados ou ocorrer erro, utiliza um CSV público da Embrapa como fallback.'
    ),
    'parameters': [
        {
            'name': 'year',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano da comercialização desejada. Caso não informado, será retornado todos os anos, ao falhar retorna nenhuma informação.'
        }
    ],
    'security': [{'BearerAuth': []}],  # Indica que o JWT é necessário
    'responses': {
        200: {
            'description': 'Lista de dados de comercialização no formato JSON',
            'examples': {
                'application/json': [
                    {
                        "Produto": "VINHO DE MESA",
                        "Quantidade (L.)": "187.016.848"
                    }
                ]
            }
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        }
    }
})
def commercialization():
    df = pd.DataFrame()  # Garante um DataFrame vazio como fallback

    try:
        if any(request.args):
            year_param = request.args.get('year')
            year = int(year_param) if year_param else datetime.datetime.today().year

            data = get_data(year, opt=4)
            df = pd.DataFrame(data)

            if df.empty:
                raise ValueError("Nenhum dado retornado pela função get_data")
        else:
            raise ValueError("Parâmetro 'year' ausente")

    except (ValueError, TypeError, Exception) as e:
        try:
            df = pd.read_csv('http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv', sep=';')
        except Exception as csv_error:
            print(f"Erro ao ler CSV de fallback: {csv_error}")
            df = pd.DataFrame()

    finally:
        return jsonify(df.to_dict(orient='records'))
