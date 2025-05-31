# 🍷 Vitivinicultura RS - API de Dados da Cadeia Vitivinícola

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Uma API completa para acesso automatizado aos dados da vitivinicultura do Rio Grande do Sul**

Este projeto fornece uma API RESTful e sistema de coleta automatizada de dados sobre produção, processamento, comercialização, importação e exportação de uvas, vinhos, sucos e derivados no **Estado do Rio Grande do Sul** - responsável por mais de **90% da produção vitivinícola brasileira**.

## ✨ Características Principais

- 🔄 **Coleta Automatizada**: Sistema de *web scraping* para dados sempre atualizados
- 📊 **API RESTful**: Endpoints organizados e documentados com Swagger
- 🛡️ **Sistema de Fallback**: Utiliza arquivos CSV como backup em caso de falhas
- 📈 **Dados Abrangentes**: Cobertura completa da cadeia vitivinícola
- 🚀 **Fácil Integração**: Respostas em JSON padronizadas

## 📋 Dados Disponíveis

### 🍇 Produção e Processamento
- Quantidade de uvas processadas por variedade
- Produção de vinhos (mesa, finos, especiais)
- Produção de sucos e derivados

### 💼 Comercialização
- Vendas no mercado interno
- Dados de comercialização por categoria

### 🌍 Comércio Internacional
- Importações detalhadas por país e categoria
- Exportações com breakdown geográfico

## 🔧 Endpoints da API

| Método | Endpoint | Descrição | Exemplo |
|--------|----------|-----------|---------|
| `GET` | `/production` | Dados de produção de vinhos e derivados | `GET /production?year=2023` |
| `GET` | `/processing` | Processamento de uvas por tipo | `GET /processing?sub=3` |
| `GET` | `/commercialization` | Comercialização no mercado interno | `GET /commercialization` |
| `GET` | `/importation` | Importações por país e categoria | `GET /importation?year=2023&sub=3` |
| `GET` | `/exportation` | Exportações detalhadas | `GET /exportation?year=2023` |

> 📖 **Documentação Completa**: Acesse `/apidocs` para ver todos os parâmetros e exemplos

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/devrictrovato/mlet-embrapa-api.git
cd mlet-embrapa-api

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute a aplicação
python app.py
```

### Testando a API

```bash
# Teste básico
curl http://localhost:5000/production

# Com parâmetros
curl "http://localhost:5000/importation?year=2023&sub=3"
```

Acesse a documentação interativa em: **http://localhost:5000/apidocs**

## 🏗️ Arquitetura do Projeto

```
mlet-embrapa-api/
├── 📁 web/
│   └── scrapping.py          # Módulos de web scraping
├── 📁 routes/
│   ├── production.py         # Endpoint de produção
│   ├── processing.py         # Endpoint de processamento
│   ├── commercialization.py  # Endpoint de comercialização
│   ├── importation.py        # Endpoint de importação
│   └── exportation.py        # Endpoint de exportação
├── 📄 app.py                 # Aplicação principal Flask
├── 📄 requirements.txt       # Dependências do projeto
└── 📄 README.md             # Este arquivo
```

## 📚 Tecnologias Utilizadas

- **[Python 3.10+](https://python.org)** - Linguagem principal
- **[Flask](https://flask.palletsprojects.com/)** - Framework web minimalista
- **[Pandas](https://pandas.pydata.org/)** - Manipulação e análise de dados
- **[Flasgger](https://github.com/flasgger/flasgger)** - Documentação Swagger automática
- **[Requests](https://requests.readthedocs.io/)** - Cliente HTTP para web scraping
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** - Parser HTML/XML

## 📊 Fontes de Dados

| Fonte | Descrição | URL |
|-------|-----------|-----|
| **Embrapa Uva e Vinho** | Dados oficiais da vitivinicultura brasileira | [vitibrasil.cnpuv.embrapa.br](http://vitibrasil.cnpuv.embrapa.br/) |
| **ALICEweb** | Dados de comércio exterior (MDIC) | [aliceweb.desenvolvimento.gov.br](http://aliceweb.desenvolvimento.gov.br/) |

## ⚠️ Notas Importantes

### 🍷 Classificação dos Vinhos
- **Vinho de mesa**: Produzido com uvas americanas ou híbridas
- **Vinho fino**: Elaborado exclusivamente com uvas *Vitis vinifera L.*
- **Vinho especial**: Blend de vinho de mesa com vinho fino

### 🌍 Dados de Importação
Os vinhos importados são classificados como "vinhos de mesa" na nomenclatura alfandegária, mas são tecnicamente equivalentes aos vinhos finos nacionais.

### ⚖️ Conversão de Unidades
Os dados da ALICEweb são fornecidos em quilogramas. Para facilitar a análise, assumimos densidade ≈ 1, convertendo **1 kg = 1 litro**.

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Casos de Uso

- **Análise de Mercado**: Identificação de tendências na produção vitivinícola
- **Pesquisa Acadêmica**: Dados estruturados para estudos econômicos
- **Business Intelligence**: Dashboards e relatórios automatizados
- **Aplicações Web**: Integração em sistemas de monitoramento
- **Data Science**: Análises preditivas e machine learning

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

**Desenvolvedor**: Ricardo Trovato  
- GitHub: [@devrictrovato](https://github.com/devrictrovato)  
- LinkedIn: [linkedin.com/in/ricardo-o-trovato/](https://www.linkedin.com/in/ricardo-o-trovato/)  
- Email: [devrictrovato@gmail.com](mailto:devrictrovato@gmail.com)

---

<div align="center">

**Desenvolvido com ❤️ para a transparência e desenvolvimento de machine learning**

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐

</div>