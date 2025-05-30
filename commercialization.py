from flask import Blueprint, jsonify, request
import pandas as pd
import datetime

from scrapping import get_data

commercialization_routes = Blueprint('commercialization', __name__)

@commercialization_routes.route('/commercialization')
def commercialization():
    df = pd.DataFrame()  # Garante um DataFrame vazio como fallback

    try:
        # Verifica se há parâmetros na requisição (?year=2023, por exemplo)
        if any(request.args):
            year_param = request.args.get('year')

            # Tenta converter o parâmetro "year" para inteiro; usa ano atual como padrão se estiver ausente
            year = int(year_param) if year_param else datetime.datetime.today().year

            # Chama a função get_data passando o ano
            data = get_data(year, opt=4)
            df = pd.DataFrame(data)

            # Se a função retornar vazio, força uso do fallback
            if df.empty:
                raise ValueError("Nenhum dado retornado pela função get_data")
        else:
            # Nenhum parâmetro informado: força uso do fallback
            raise ValueError("Parâmetro 'year' ausente")

    except (ValueError, TypeError, Exception) as e:
        try:
            # Fallback: tenta carregar o CSV padrão diretamente do site da Embrapa
            df = pd.read_csv('http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv', sep=';')
        except Exception as csv_error:
            # Caso o download ou leitura do CSV falhe, retorna DataFrame vazio
            print(f"Erro ao ler CSV de fallback: {csv_error}")
            df = pd.DataFrame()

    finally:
        # Retorna a resposta sempre como JSON, mesmo que vazia
        return jsonify(df.to_dict(orient='records'))
