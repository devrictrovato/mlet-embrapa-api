import pandas as pd
import datetime

from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_jwt_extended import verify_jwt_in_request

from web.scrapping import get_data

production_routes = Blueprint('production_routes', __name__)

# 🔐 Protege todas as rotas com JWT
@production_routes.before_request
def require_jwt():
    verify_jwt_in_request()

@production_routes.route('/production')
@swag_from({
    'tags': ['Vitivinicultura'],
    'summary': 'Retorna dados de produção vitivinícola por ano.',
    'description': (
        'Esta rota requer autenticação JWT. '
        'Busca dados de produção vitivinícola com base no ano fornecido como parâmetro. '
        'Se não houver dados disponíveis pela função `get_data`, é usado um CSV online como fallback.'
    ),
    'parameters': [
        {
            'name': 'year',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano desejado. Se não informado, tenta o ano atual. Fallback para CSV se falhar.'
        }
    ],
    'security': [{'BearerAuth': []}],  # 👈 Requer JWT no Swagger
    'responses': {
        200: {
            'description': 'Dados de produção em formato JSON',
            'examples': {
                'application/json': [
                    {
                        "Produto": "VINHO DE MESA",
                        "Quantidade (L.)": "169.762.429"
                    }
                ]
            }
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        }
    }
})
def production():
    df = pd.DataFrame()

    try:
        if any(request.args):
            year_param = request.args.get('year')
            year = int(year_param) if year_param else datetime.datetime.today().year

            data = get_data(year, opt=2)
            df = pd.DataFrame(data)

            if df.empty:
                raise ValueError("Nenhum dado retornado pela função get_data")
        else:
            raise ValueError("Parâmetro 'year' ausente")

    except (ValueError, TypeError, Exception) as e:
        try:
            df = pd.read_csv('http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv', sep=';')
        except Exception as csv_error:
            print(f"Erro ao ler CSV de fallback: {csv_error}")
            df = pd.DataFrame()

    finally:
        return jsonify(df.to_dict(orient='records'))
