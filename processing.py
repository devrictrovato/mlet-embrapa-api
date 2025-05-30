from flask import Blueprint, request, jsonify
import pandas as pd
import datetime

from scrapping import get_data

processing_routes = Blueprint('processing', __name__)

@processing_routes.route('/processing')
def processing():
    df = pd.DataFrame()  # Garante um DataFrame vazio como fallback

    try:
        # Verifica se há qualquer parâmetro na requisição (ex: ?year=2023&sub=1)
        if any(request.args):
            year_param = request.args.get('year')
            suboption_param = request.args.get('sub')

            # Usa o ano atual como padrão se "year" não for fornecido
            year = int(year_param) if year_param else datetime.datetime.today().year
            # Usa 0 como padrão se "sub" não for fornecido
            suboption = int(suboption_param) if suboption_param else 0

            # Chama a função get_data com os parâmetros resolvidos
            data = get_data(year, opt=3, subopt=suboption)
            df = pd.DataFrame(data)

        else:
            # Se nenhum parâmetro for passado, usa os arquivos CSV como fallback
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
        df = pd.DataFrame()  # Fallback final para erro

    return jsonify(df.to_dict(orient='records'))
