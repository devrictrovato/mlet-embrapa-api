import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_data(year: int = 2023, opt: int = 2, subopt: int = 0) -> pd.DataFrame:
    """
    Obtém dados tabulares do site VitiBrasil (Embrapa) conforme parâmetros fornecidos.

    Esta função monta uma URL dinâmica baseada nos parâmetros, acessa a página web pública da Embrapa,
    faz o scraping da tabela HTML específica, e retorna os dados como um DataFrame do pandas.

    Parâmetros:
    ----------
    year : int, opcional (padrão=2023)
        Ano base para consulta dos dados.

    opt : int, opcional (padrão=2)
        Código da opção principal do menu (ex: 1 para 'opt_01', 2 para 'opt_02').

    subopt : int, opcional (padrão=0)
        Código da subopção para refinar a consulta. Se 0, não é incluído na URL.

    Retorno:
    -------
    pd.DataFrame
        DataFrame com os dados extraídos da tabela HTML.
        Se a extração falhar, retorna um DataFrame vazio.

    Observação:
    -----------
    A função depende da estrutura HTML atual do site da Embrapa. Alterações no site podem impactar seu funcionamento.
    """

    # Inicializa DataFrame vazio para retorno caso ocorra erro
    df = pd.DataFrame()

    # Formata os parâmetros 'opt' e 'subopt' no formato esperado pela URL (ex: 'opt_02', 'subopt_01')
    formated_opt = f"opt_{opt:02d}"
    formated_subopt = f"subopt_{subopt:02d}"

    # Monta a URL base com o ano e opção principal
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao={formated_opt}"

    # Caso subopt seja maior que zero, adiciona o parâmetro subopt à URL
    if subopt > 0:
        url = f"{url}&subopcao={formated_subopt}"

    try:
        # Faz a requisição HTTP para obter o conteúdo da página
        response = requests.get(url)
        response.raise_for_status()  # Levanta exceção para status HTTP ruim

        # Parseia o conteúdo HTML da página usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Localiza a tabela com a classe CSS específica que contém os dados
        table = soup.find('table', {'class': 'tb_base tb_dados'})

        # Extrai todas as linhas da tabela
        rows = table.find_all('tr')

        # Lista para armazenar os dados extraídos da tabela
        data = []

        # Percorre cada linha, extraindo o texto das células (tanto cabeçalhos quanto dados)
        for row in rows:
            cells = row.find_all(['th', 'td'])
            cells_text = [cell.get_text(strip=True) for cell in cells]
            data.append(cells_text)

        # Cria o DataFrame usando a primeira linha como cabeçalho e o restante como dados
        df = pd.DataFrame(data[1:], columns=data[0])

        # Retorna o DataFrame com os dados extraídos
        return df

    except Exception as e:
        # Em caso de erro (ex: mudança na página, falta da tabela, falha na requisição), retorna DataFrame vazio
        # Para debug, descomente a linha abaixo:
        # print(f"Erro ao obter os dados: {e}")
        return df
