# Aedem API

**Aedem** é uma API (application programming interface) escrita para gerenciar as inspeções, denúncias e demais dados gerados através das aplicações do Programa de Extensão Aedes Zero, na Universidade Federal do Espírito Santo (UFES).

# Instalação

Essa API está em desenvolvimento e não é apropriada para uso em produção nesse momento.

## Requisitos

Essa API foi desenvolvida usando Python 3.8. Para instalar os requisitos da API, use:

```
$ python3.8 -m pip install -r requirements.txt
```

## Rodando em modo de desenvolvimento

Modifique as configurações em ```config/development.py``` com as informações de conexão ao banco de dados. Caso queira alterar as configurações padrões, modifique-as em ```config/__init__.py```.

Após configurar a API, configure a variável de ambiente ```FLASK_ENV``` para ```development```. Em sistemas derivados do Debian:

```
$ export FLASK_ENV=development
```

Feito isso, rode a aplicação:

```
$ python3.8 app.py
```

# Autores

- Carlos H. R. Barbosa \([@henriquerubia](https://github.com/henriquerubia "Henrique Rubia")\)
- Kleiton C. A. Santos \([@kleitonv3](https://github.com/kleitonv3 "Kleiton Cássio")\)
- Ailton J. B. Junior \([@Junior41](https://github.com/kleitonv3 "A.J.B. Junior")\)

# Licença

```
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
```