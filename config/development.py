from config import BaseConfig

class Config(BaseConfig):
    # Configurações de debug
    # (modo de produção/development deve ser configurado pela variável de
    #  ambiente FLASK_ENV, veja README.md)
    DEBUG           = True

    # Configurações do banco de dados
    DB_DIALECT      = "postgresql"
    DB_HOST         = "localhost"
    DB_PORT         = 5432
    DB_NAME         = "aedem"
    DB_USERNAME     = ""
    DB_PASSWORD     = ""