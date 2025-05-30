from flask import Blueprint, request, jsonify
import pandas as pd
import datetime

from scrapping import get_data

importation_routes = Blueprint('importation', __name__)

@importation_routes.route('/importation')
def importation():
    df = pd.DataFrame()  # Fallback inicial: DataFrame vazio

    try:
        # Verifica se há parâmetros fornecidos na requisição (?year=2023&sub=1)
        if any(request.args):
            year_param = request.args.get('year')
            sub_param = request.args.get('sub')

            # Converte os parâmetros, com valores padrão se não informados
            year = int(year_param) if year_param else datetime.datetime.today().year
            suboption = int(sub_param) if sub_param else 0

            # Chama a função get_data com opt=1 (importação) e subopção correspondente
            data = get_data(year, opt=5, subopt=suboption)
            df = pd.DataFrame(data)

            # Se nada for retornado, força uso do fallback
            if df.empty:
                raise ValueError("Nenhum dado retornado pela função get_data")
        else:
            # Nenhum parâmetro fornecido: faz o fallback com os CSVs públicos da Embrapa
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

    # Sempre retorna uma resposta JSON válida, mesmo se estiver vazia
    return jsonify(df.to_dict(orient='records'))
