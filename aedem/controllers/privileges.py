from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields

from aedem.utils import dictionarize

from aedem.models import Session
from aedem.models.privileges import Privilege

namespace = Namespace(
    'privileges',
    path = "/privileges",
    description = 'Operações de controle de privilégios'
)

create_privilege_model = namespace.model("create_privilege", {
    "identifier": fields.String(
        description = "Identificador do privilégio",
        required = True),
    "assignable": fields.Boolean(
        description = "Permissão para conceder esse privilégio",
        required = False)
})

@namespace.route('')
class PrivilegeList(Resource):
    @namespace.doc('list_privileges')
    def get(self):
        '''Lista todos os privilégios'''
        session = Session()

        # get list of privileges
        privileges = []
        for privilege in session.query(Privilege).all():
            privileges.append(dictionarize(privilege))
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": privileges
        }
        return jsonify(response)
    
    @namespace.doc('create_privilege')
    @namespace.expect(create_privilege_model)
    def post(self):
        '''Cria um novo privilégio'''
        session = Session()

        # get privilege information provided in the request
        privilege_data = request.get_json(force = True)

        # create database model
        new_privilege = Privilege(
            identifier = privilege_data['identifier'],
            assignable = privilege_data['assignable']
        )

        # add new privilege entity to database
        session.add(new_privilege)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(new_privilege)
        }
        return jsonify(response)

@namespace.route('/<id>')
@namespace.param('id', 'Identificador do privilégio')
@namespace.response(404, 'Privilégio não encontrado')
class SpecificPrivilege(Resource):
    @namespace.doc('get_privilege')
    def get(self, id):
        '''Mostra um privilégio específico'''
        session = Session()

        privilege = session.query(Privilege).filter_by(identifier = id).first()
        if privilege is None:
            namespace.abort(404)
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(privilege)
        }
        return jsonify(response)

    @namespace.doc('delete_privilege')
    def delete(self, id):
        '''Deleta um privilégio'''
        session = Session()

        # look up given privilege
        given_privilege = session.query(Privilege).filter_by(identifier = id)

        # check if given privilege exists
        if given_privilege.scalar() is None:
            namespace.abort(404)

        # delete privilege entry from database
        privilege = given_privilege.one()
        records = dictionarize(privilege)
        session.delete(privilege)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": records
        }
        return jsonify(response)

    @namespace.doc('update_privilege')
    def put(self, id):
        '''Atualiza os dados de um privilégio'''
        session = Session()

        # look up given privilege
        given_privilege = session.query(Privilege).filter_by(identifier = id)

        # check if given privilege exists
        if given_privilege.scalar() is None:
            namespace.abort(404)

        # update privilege entry with given values
        privilege = given_privilege.one()

        for datafield in request.args:
            setattr(privilege, datafield, request.args[datafield])

        session.add(privilege)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(privilege)
        }
        return jsonify(response)
