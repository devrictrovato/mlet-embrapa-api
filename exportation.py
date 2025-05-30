from flask import Blueprint, request, jsonify
import pandas as pd
import datetime

from scrapping import get_data

exportation_routes = Blueprint('exportation', __name__)

@exportation_routes.route('/exportation')
def exportation():
    df = pd.DataFrame()  # Fallback inicial: DataFrame vazio

    try:
        # Verifica se a requisição inclui parâmetros (?year=2023&sub=1)
        if any(request.args):
            year_param = request.args.get('year')
            sub_param = request.args.get('sub')

            # Converte os parâmetros para inteiro, usando valores padrão caso estejam ausentes
            year = int(year_param) if year_param else datetime.datetime.today().year
            suboption = int(sub_param) if sub_param else 0

            # Chama a função get_data com opt=4 (exportação)
            data = get_data(year, opt=6, subopt=suboption)
            df = pd.DataFrame(data)

            # Se nada for retornado, força fallback para os CSVs
            if df.empty:
                raise ValueError("Nenhum dado retornado pela função get_data")
        else:
            # Nenhum parâmetro informado: faz o fallback com os CSVs públicos da Embrapa
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
        df = pd.DataFrame()  # Fallback final: garante um DataFrame vazio

    # Sempre retorna uma resposta JSON válida, mesmo que vazia
    return jsonify(df.to_dict(orient='records'))
