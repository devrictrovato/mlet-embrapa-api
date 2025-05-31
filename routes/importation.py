import pandas as pd
import datetime

from flask import Blueprint, request, jsonify
from flasgger import swag_from

from web.scrapping import get_data

importation_routes = Blueprint('importation', __name__)

@importation_routes.route('/importation')
@swag_from({
    'tags': ['Importação'],
    'summary': 'Retorna dados de importação de produtos vitivinícolas por ano e subcategoria.',
    'description': 'Consulta os dados de importação conforme os parâmetros informados. '
                   'Se nenhum parâmetro for fornecido ou ocorrer erro, são utilizados arquivos CSV públicos da Embrapa como fallback.',
    'parameters': [
        {
            'name': 'year',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano da importação. Se não for informado, o ano atual será utilizado'
        },
        {
            'name': 'sub',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Subcategoria da importação. Padrão é 0 se não fornecido'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de dados de importação no formato JSON',
            'examples': {
                'application/json': [
                    {
                        "Países": "Africa do Sul",
                        "Quantidade (Kg)": "522.733",
                        "Valor (US$)": "1.732.850"
                    }
                ]
            }
        }
    }
})
def importation():
    df = pd.DataFrame()  # Fallback inicial: DataFrame vazio

    try:
        if any(request.args):
            year_param = request.args.get('year')
            sub_param = request.args.get('sub')

            year = int(year_param) if year_param else datetime.datetime.today().year
            suboption = int(sub_param) if sub_param else 0

            data = get_data(year, opt=5, subopt=suboption)
            df = pd.DataFrame(data)

            if df.empty:
                raise ValueError("Nenhum dado retornado pela função get_data")
        else:
            urls = [
                ('http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv', '\t'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv', '\t'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv', '\t'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv', '\t'),
                ('http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv', ';')
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
        df = pd.DataFrame()  # Fallback final: garante DataFrame vazio

    return jsonify(df.to_dict(orient='records'))
