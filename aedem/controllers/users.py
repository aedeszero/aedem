from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields

from aedem.utils import dictionarize

from aedem.models import Session
from aedem.models.users import User

namespace = Namespace(
    'users',
    path = "/users",
    description = 'Operações de usuários'
)

create_user_model = namespace.model("create_user", {
    "name": fields.String(
        description = "Nome do usuário",
        required = True),
    "email": fields.String(
        description = "Endereço de Email do usuário",
        required = True),
    "phone": fields.Integer(
        description = "Número de Celular do usuário",
        required = True),
    "passhash": fields.String(
        description = "Hash da senha do usuário", 
        required = True),
    "salt": fields.String(
        description = "Salt da senha do usuário",
        required = True),
    "birthday": fields.String(
        description = "Data de aniversário do usuário",
        required = True),
    "zip_code": fields.String(
        description = "CEP do usuário",
        required = True),
    "state_abbr": fields.String(
        description = "Estado do usuário",
        required = True),
    "city_name": fields.String(
        description = "Nome da cidade do usuário",
        required = True),
    "city_number": fields.Integer(
        description = "Número da cidade do usuário",
        required = False),
    "area": fields.String(
        description = "Bairro/area da cidade do usuário",
        required = True)
})

@namespace.route('/')
class UserList(Resource):
    @namespace.doc('list_users')
    def get(self):
        '''Listagem de todos os usuários'''
        session = Session()

        # get list of users
        users = []
        for user in session.query(User).all():
            users.append(dictionarize(user))
        
        return jsonify(users)
    
    @namespace.doc('create_user')
    @namespace.expect(create_user_model)
    def post(self):
        '''Cria um novo usuário'''
        session = Session()

        # get user data provided in the request
        userdata = request.get_json(force = True)

        # create database model
        new_user = User(
            name = userdata['name'],
            email = userdata['email'],
            phone = userdata['phone'],
            passhash = userdata['passhash'],
            salt = userdata['salt'],
            birthday = userdata['birthday'],
            zip_code = userdata['zip_code'],
            state_abbr = userdata['state_abbr'],
            city_name = userdata['city_name'],
            city_number = userdata['city_number'],
            area = userdata['area']
        )

        # add new user to database
        session.add(new_user)
        session.commit()

        # response
        return jsonify(dictionarize(new_user))

@namespace.route('/<id>')
@namespace.param('id', 'Identificador do usuário')
@namespace.response(404, 'Usuário não encontrado')
class SpecificUser(Resource):
    @namespace.doc('get_user')
    def get(self, id):
        '''Mostrar um usuário específico'''
        session = Session()

        user = session.query(User).filter_by(id = id).first()
        if user is not None:
            return jsonify(dictionarize(user))
        else:
            namespace.abort(404)