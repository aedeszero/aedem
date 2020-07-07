from flask import jsonify
from flask_restplus import Namespace, Resource, fields

from aedem.utils import dictionarize

from aedem.models import Session
from aedem.models.users import User

namespace = Namespace(
    'users',
    path = "/users",
    description = 'Operações de usuários'
)

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