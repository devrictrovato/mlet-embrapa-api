import pandas as pd
import datetime

from flask import Blueprint, jsonify, request
from flasgger import swag_from

from web.scrapping import get_data

commercialization_routes = Blueprint('commercialization', __name__)

@commercialization_routes.route('/commercialization')
@swag_from({
    'tags': ['Comercialização'],
    'summary': 'Retorna dados de comercialização de produtos vitivinícolas por ano.',
    'description': 'Busca dados de comercialização usando o ano informado como parâmetro. '
                   'Se a função `get_data` não retornar dados ou ocorrer erro, utiliza um CSV público da Embrapa como fallback.',
    'parameters': [
        {
            'name': 'year',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano da comercialização desejada. Caso não informado, será retornado todos os anos, ao falhar retorna nenhuma informação.'
        }
    ],
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
