import pandas as pd
import datetime

from flask import Blueprint, request, jsonify
from flasgger import swag_from

from web.scrapping import get_data

from flask_jwt_extended import verify_jwt_in_request

exportation_routes = Blueprint('exportation', __name__)

# Aplica verificação JWT a todas as rotas do blueprint
@exportation_routes.before_request
def require_jwt():
    verify_jwt_in_request()

@exportation_routes.route('/exportation')
@swag_from({
    'tags': ['Vitivinicultura'],
    'summary': 'Retorna dados de exportação de produtos vitivinícolas por ano e subcategoria.',
    'description': (
        'Esta rota requer autenticação JWT.\n'
        'Consulta os dados de exportação com base nos parâmetros fornecidos (ano e subcategoria). '
        'Caso os dados da função `get_data` estejam indisponíveis, utiliza arquivos CSV públicos da Embrapa como fallback.'
    ),
    'parameters': [
        {
            'name': 'year',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano da exportação. Se não for informado, o ano atual será utilizado.'
        },
        {
            'name': 'sub',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Subcategoria da exportação (ex: vinho, espumante, uva, suco). Padrão: 0.'
        }
    ],
    'security': [{'BearerAuth': []}],  # Indica que JWT é necessário
    'responses': {
        200: {
            'description': 'Lista de dados de exportação no formato JSON',
            'examples': {
                'application/json': [
                    {
                        "Países": "África do Sul",
                        "Quantidade (Kg)": "117",
                        "Valor (US$)": "698"
                    }
                ]
            }
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        }
    }
})
def exportation():
    df = pd.DataFrame()  # Fallback inicial: DataFrame vazio

    try:
        if any(request.args):
            year_param = request.args.get('year')
            sub_param = request.args.get('sub')

            year = int(year_param) if year_param else datetime.datetime.today().year
            suboption = int(sub_param) if sub_param else 0

            data = get_data(year, opt=6, subopt=suboption)
            df = pd.DataFrame(data)

            if df.empty:
                raise ValueError("Nenhum dado retornado pela função get_data")
        else:
            urls = [
                ('http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv', '\t'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv', '\t'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv', '\t'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv', '\t')
            ]

            frames = []
            for url, sep in urls:
                try:
                    temp_df = pd.read_csv(url, sep=sep)
                    if not temp_df.empty:
                        frames.append(temp_df)
                except Exception as e:
                    print(f"Erro ao carregar {url}: {e}")

            if frames:
                df = pd.concat(frames, ignore_index=True)
            else:
                raise ValueError("Nenhum dado foi carregado dos arquivos CSV")

    except Exception as e:
        print(f"Erro geral: {e}")
        df = pd.DataFrame()

    return jsonify(df.to_dict(orient='records'))
