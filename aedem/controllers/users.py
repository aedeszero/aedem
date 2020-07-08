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

@namespace.route('')
class UserList(Resource):
    @namespace.doc('list_users')
    def get(self):
        '''Listagem de todos os usuários'''
        session = Session()

        # get list of users
        users = []
        for user in session.query(User).all():
            users.append(dictionarize(user))
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": users
        }
        return jsonify(response)
    
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

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(new_user)
        }
        return jsonify(response)

@namespace.route('/<id>')
@namespace.param('id', 'Identificador do usuário')
@namespace.response(404, 'Usuário não encontrado')
class SpecificUser(Resource):
    @namespace.doc('get_user')
    def get(self, id):
        '''Mostrar um usuário específico'''
        session = Session()

        user = session.query(User).filter_by(id = id).first()
        if user is None:
            namespace.abort(404)
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(user)
        }
        return jsonify(response)

    @namespace.doc('delete_user')
    def delete(self, id):
        '''Deleta um usuário existente'''
        session = Session()

        # look up given user
        given_user = session.query(User).filter_by(id = id)

        # check if given user exists
        if given_user.scalar() is None:
            namespace.abort(404)

        # delete user from database
        user = given_user.one()
        records = dictionarize(user)
        session.delete(user)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": records
        }
        return jsonify(response)

    @namespace.doc('update_user')
    def put(self, id):
        '''Atualiza os dados de um usuário'''
        session = Session()

        # look up given user
        given_user = session.query(User).filter_by(id = id)

        # check if given user exists
        if given_user.scalar() is None:
            namespace.abort(404)

        # update user data with given values
        user = given_user.one()

        for datafield in request.args:
            setattr(user, datafield, request.args[datafield])

        session.add(user)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(user)
        }
        return jsonify(response)
