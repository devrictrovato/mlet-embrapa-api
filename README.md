# 🍷 Vitivinicultura RS - API de Dados da Cadeia Vitivinícola

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![JWT](https://img.shields.io/badge/JWT-Enabled-orange.svg)](https://jwt.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Uma API completa e segura para acesso automatizado aos dados da vitivinicultura do Rio Grande do Sul**

Este projeto fornece uma API RESTful protegida por JWT e sistema de coleta automatizada de dados sobre produção, processamento, comercialização, importação e exportação de uvas, vinhos, sucos e derivados no **Estado do Rio Grande do Sul** - responsável por mais de **90% da produção vitivinícola brasileira**.

## ✨ Características Principais

- 🔐 **Autenticação JWT**: Sistema seguro de autenticação com tokens
- 🔄 **Coleta Automatizada**: Sistema de *web scraping* para dados sempre atualizados
- 📊 **API RESTful**: Endpoints organizados e documentados com Swagger
- 🛡️ **Sistema de Fallback**: Utiliza arquivos CSV como backup em caso de falhas
- 📈 **Dados Abrangentes**: Cobertura completa da cadeia vitivinícola
- 🚀 **Fácil Integração**: Respostas em JSON padronizadas

## 🔐 Autenticação

A API utiliza **JSON Web Tokens (JWT)** para autenticação. Você precisa obter um token válido antes de acessar os endpoints protegidos.

### Login e Obtenção do Token

```bash
# Fazer login e obter o token JWT
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "password": "sua_senha"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "Login realizado com sucesso",
  "expires_in": 3600
}
```

### Usando o Token

Inclua o token no cabeçalho `Authorization` de todas as requisições:

```bash
curl -H "Authorization: Bearer SEU_TOKEN_JWT" \
  http://localhost:5000/production
```

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

### 🔓 Endpoints Públicos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/login` | Autenticação e obtenção do token JWT |

### 🔒 Endpoints Protegidos (Requerem JWT)

| Método | Endpoint | Descrição | Exemplo |
|--------|----------|-----------|---------|
| `GET` | `/production` | Dados de produção de vinhos e derivados | `GET /production?year=2023` |
| `GET` | `/processing` | Processamento de uvas por tipo | `GET /processing?sub=3` |
| `GET` | `/commercialization` | Comercialização no mercado interno | `GET /commercialization` |
| `GET` | `/importation` | Importações por país e categoria | `GET /importation?year=2023&sub=3` |
| `GET` | `/exportation` | Exportações detalhadas | `GET /exportation?year=2023` |

> 📖 **Documentação Completa**: Acesse `/apidocs` para ver todos os parâmetros e exemplos
> 🔐 **Observação**: A documentação Swagger também requer autenticação JWT

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

# 5. Configure as variáveis de ambiente (opcional)
# Crie um arquivo .env com:
# JWT_SECRET_KEY=sua_chave_secreta_jwt
# JWT_EXPIRATION_HOURS=24

# 6. Execute a aplicação
python app.py
```

### Testando a API

```bash
# 1. Primeiro, faça login e obtenha o token
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"seu_usuario","password":"sua_senha"}' \
  | jq -r '.access_token')

# 2. Use o token para acessar os endpoints protegidos
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/production

# 3. Com parâmetros
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:5000/importation?year=2023&sub=3"
```

### Exemplo com Python

```python
import requests

# 1. Fazer login
login_data = {
    "username": "seu_usuario",
    "password": "sua_senha"
}

response = requests.post("http://localhost:5000/login", json=login_data)
token = response.json()["access_token"]

# 2. Usar o token para acessar dados
headers = {"Authorization": f"Bearer {token}"}
production_data = requests.get("http://localhost:5000/production", headers=headers)

print(production_data.json())
```

Acesse a documentação interativa em: **http://localhost:5000/apidocs**

## 🏗️ Arquitetura do Projeto

```
mlet-embrapa-api/
├── 📁 auth/
│   └── authentication.py     # Middleware de autenticação JWT
├── 📁 db/
│   ├── authentication.py     # Banco de dados sqlite
│   └── model.py              # Modelos ORM
├── 📁 templates/
│   ├── index.html            # Painel principal da api
│   └── login.html            # Sistema de login jwt
├── 📁 web/
│   └── scrapping.py          # Módulos de web scraping
├── 📁 routes/
│   ├── auth.py               # Endpoint de autenticação
│   ├── production.py         # Endpoint de produção
│   ├── processing.py         # Endpoint de processamento
│   ├── commercialization.py  # Endpoint de comercialização
│   ├── importation.py        # Endpoint de importação
│   └── exportation.py        # Endpoint de exportação
├── 📄 app.py                 # Aplicação principal Flask
├── 📄 config.py              # Configurações do flask
├── 📄 pyproject.toml         # Dependências do projeto
└── 📄 README.md              # Este arquivo
```

## 📚 Tecnologias Utilizadas

- **[Python 3.10+](https://python.org)** - Linguagem principal
- **[Flask](https://flask.palletsprojects.com/)** - Framework web minimalista
- **[PyJWT](https://pyjwt.readthedocs.io/)** - Implementação JWT para Python
- **[Pandas](https://pandas.pydata.org/)** - Manipulação e análise de dados
- **[Flasgger](https://github.com/flasgger/flasgger)** - Documentação Swagger automática
- **[Requests](https://requests.readthedocs.io/)** - Cliente HTTP para web scraping
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** - Parser HTML/XML

## 🔒 Segurança

### Configuração JWT

A API utiliza as seguintes configurações de segurança:

- **Algoritmo**: HS256 (HMAC com SHA-256)
- **Expiração padrão**: 1 hora (configurável)
- **Chave secreta**: Configurável via variável de ambiente

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Chave secreta para assinatura JWT (obrigatória)
JWT_SECRET_KEY=sua_chave_secreta_muito_forte_aqui

# Tempo de expiração do token em horas (opcional, padrão: 1)
JWT_EXPIRATION_HOURS=24

# Configurações da aplicação
FLASK_ENV=production
FLASK_DEBUG=False
```

### Boas Práticas

- ✅ Mantenha a chave JWT secreta e segura
- ✅ Use HTTPS em produção
- ✅ Configure tempos de expiração apropriados
- ✅ Implemente rotação de tokens se necessário
- ✅ Monitore tentativas de acesso não autorizadas

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

### 🔐 Autenticação
- Todos os endpoints de dados requerem autenticação JWT
- Tokens têm tempo de expiração configurável
- Implemente renovação de tokens conforme necessário

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
- **Aplicações Web**: Integração segura em sistemas de monitoramento
- **Data Science**: Análises preditivas e machine learning
- **APIs Corporativas**: Integração segura com sistemas empresariais

## 🚨 Tratamento de Erros

### Códigos de Status HTTP

| Código | Descrição | Quando Ocorre |
|--------|-----------|---------------|
| `200` | Sucesso | Requisição processada com sucesso |
| `400` | Bad Request | Parâmetros inválidos ou formato incorreto |
| `401` | Unauthorized | Token JWT ausente, inválido ou expirado |
| `403` | Forbidden | Acesso negado (credenciais válidas, mas sem permissão) |
| `404` | Not Found | Endpoint não encontrado |
| `500` | Internal Server Error | Erro interno do servidor |

### Exemplos de Resposta de Erro

```json
// Token ausente ou inválido
{
  "error": "Token de acesso requerido",
  "code": 401
}

// Token expirado
{
  "error": "Token expirado. Faça login novamente.",
  "code": 401
}

// Credenciais inválidas no login
{
  "error": "Credenciais inválidas",
  "code": 401
}
```

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