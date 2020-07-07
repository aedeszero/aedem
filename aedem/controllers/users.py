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