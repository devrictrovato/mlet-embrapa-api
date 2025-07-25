import pandas as pd
import datetime

from flask import Blueprint, request, jsonify
from flasgger import swag_from

from web.scrapping import get_data

from flask_jwt_extended import verify_jwt_in_request

processing_routes = Blueprint('processing', __name__)

# Protege todas as rotas com JWT
@processing_routes.before_request
def require_jwt():
    verify_jwt_in_request()

@processing_routes.route('/processing')
@swag_from({
    'tags': ['Vitivinicultura'],
    'summary': 'Retorna dados de processamento de uvas por ano e subcategoria.',
    'description': (
        'Esta rota requer autenticação JWT.\n'
        'Consulta os dados de processamento de uvas conforme os parâmetros informados. '
        'Caso nenhum parâmetro seja fornecido, dados de múltiplas fontes CSV são utilizados como fallback.'
    ),
    'parameters': [
        {
            'name': 'year',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano para o qual se deseja obter os dados de processamento. Caso não informado, retorna todos os dados, ao falhar retorna nenhuma informação.'
        },
        {
            'name': 'sub',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Subcategoria do processamento. Padrão é 0 se não fornecido, ao falhar retorna nenhuma informação.'
        }
    ],
    'security': [{'BearerAuth': []}],  # <-- Indica que rota exige JWT Bearer
    'responses': {
        200: {
            'description': 'Lista de dados de processamento no formato JSON',
            'examples': {
                'application/json': [
                    {
                        "Cultivar": "TINTAS",
                        "Quantidade (Kg)": "35.881.118"
                    }
                ]
            }
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        }
    }
})
def processing():
    df = pd.DataFrame()  # fallback

    try:
        if any(request.args):
            year_param = request.args.get('year')
            suboption_param = request.args.get('sub')

            year = int(year_param) if year_param else datetime.datetime.today().year
            suboption = int(suboption_param) if suboption_param else 0

            data = get_data(year, opt=3, subopt=suboption)
            df = pd.DataFrame(data)

        else:
            urls = [
                ('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv', ';'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv', '\t'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv', '\t'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv', '\t')
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
                raise ValueError("Nenhum dado foi carregado dos CSVs")

    except Exception as e:
        print(f"Erro geral: {e}")
        df = pd.DataFrame()

    return jsonify(df.to_dict(orient='records'))
