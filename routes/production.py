import pandas as pd
import datetime

from flask import Blueprint, request, jsonify
from flasgger import swag_from

from web.scrapping import get_data

production_routes = Blueprint('production_routes', __name__)

@production_routes.route('/production')
@swag_from({
    'tags': ['Produção'],
    'summary': 'Retorna dados de produção vitivinícola por ano.',
    'description': 'Busca dados de produção usando o ano informado como parâmetro. '
                   'Se não houver dados disponíveis pela função `get_data`, um fallback para um CSV online será utilizado.',
    'parameters': [
        {
            'name': 'year',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano para o qual se deseja obter os dados de produção. Caso não informado, retorna todos os dados, ao falhar retorna nenhuma informação.'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de dados de produção no formato JSON',
            'examples': {
                'application/json': [
                    {
                        "Produto": "VINHO DE MESA",
                        "Quantidade (L.)": "169.762.429"
                    }
                ]
            }
        }
    }
})
def production():
    df = pd.DataFrame()  # Garante um DataFrame vazio como fallback inicial

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
