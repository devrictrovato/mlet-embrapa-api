import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_data(age: int = 2023, opt: int = 2, subopt: int = 0) -> pd.DataFrame:
    """
    Obtém dados tabulares da plataforma do projeto VitiBrasil (Embrapa) com base nos parâmetros fornecidos.

    Este endpoint acessa uma página web pública da Embrapa VitiBrasil, formata a URL conforme os parâmetros
    fornecidos e extrai os dados de uma tabela HTML. Os dados retornados são convertidos para o formato JSON.

    Parâmetros:
    ----------
    age : int, opcional (padrão=2023)
        Ano de referência para a consulta dos dados.

    opt : int, opcional (padrão=2)
        Código da opção principal do menu (e.g., 1 para "opt_01", 2 para "opt_02", etc.).

    subopt : int, opcional (padrão=0)
        Código da subopção. Se maior que zero, será incluído como parâmetro adicional na URL para refinar a consulta.

    Retorno:
    -------
    pd.DataFrame
        Dados extraídos da tabela, convertidos para JSON no formato de lista de registros.
        Se não for possível extrair os dados (por erro na página ou estrutura inesperada), retorna um JSON representando um DataFrame vazio.

    Observação:
    ----------
    Este método depende da estrutura HTML da página da Embrapa. Mudanças no site podem afetar o funcionamento.
    """

    # Inicializa os dados para retorno
    df = pd.DataFrame()

    # Formata os parâmetros 'opt' e 'subopt' no padrão requerido pela URL (e.g., 'opt_01')
    formated_opt = f"opt_{opt:02d}"
    formated_subopt = f"subopt_{subopt:02d}"

    # Monta a URL base sem subopcao
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?age={age}&opcao={formated_opt}"

    # Se subopt for maior que zero, adiciona o parâmetro 'subopcao' à URL
    if subopt > 0:
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?age={age}&opcao={formated_opt}&subopcao={formated_subopt}"

    try:
        # Requisição da url
        response = requests.get(url)

        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()

        # Parseia o HTML da página usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra a tabela específica pela class
        table = soup.find('table', {'class': 'tb_base tb_dados'})

        # Extrai as linhas da tabela
        rows = table.find_all('tr')

        # Lista para armazenar os dados
        data = []

        # Itera sobre as linhas e extrai o texto das células
        for row in rows:
            cells = row.find_all(['th', 'td']) # Inclui cabeçalhos (th) e dados (td)
            cells_text = [cell.get_text(strip=True) for cell in cells]
            data.append(cells_text)

        # Converte os dados em um DataFrame do pandas
        df = pd.DataFrame(data[1:], columns=data[0]) # A linha 0 é cabeçalho

        # Converte o DataFrame para JSON no formato de lista de registros
        return df.to_json(orient="records", force_ascii=False)

    except Exception as e:
        # Em caso de erro, retorna um DataFrame vazio em formato JSON
        # Para depuração, o erro pode ser impresso descomentando a linha abaixo
        # print(f"Erro ao obter os dados: {e}")
        return df.to_json(orient="records")
