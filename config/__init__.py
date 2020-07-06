class BaseConfig(object):
    # Configurações gerais da aplicação
    APP_NAME        = "Aedem"
    APP_VERSION     = "v1"
    APP_DESCRIPTION = "API para gerenciar os dados em todas aplicações do Aedes Zero"
    
    # Configuração de resources e URL
    BASE_URL        = "/api/v1"
    DOCS_RESOURCE   = "/docs"

    # Configurações de debug
    # (modo de produção/development deve ser configurado pela variável de
    #  ambiente FLASK_ENV, veja README.md)
    DEBUG           = False
    TESTING         = False
    
    # Configurações do banco de dados
    DB_DIALECT      = "postgresql"
    DB_HOST         = "localhost"
    DB_PORT         = 5432
    DB_NAME         = "aedem"
    DB_USERNAME     = ""
    DB_PASSWORD     = ""