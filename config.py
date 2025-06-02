class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    # Use uma variável de ambiente para melhor segurança do projeto e não deixar o segredo diretamente no código.
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'chave-padrao-insegura')
    JWT_SECRET_KEY = '6fe4fbe5c833d787fb97c2211cfa6f8eef0437ebf4052c7e9eff6de008205443'
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
