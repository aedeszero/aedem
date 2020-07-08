from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields

from aedem.utils import dictionarize

from aedem.models import Session
from aedem.models.flags import Flag
from aedem.models.privileges import Privilege

namespace = Namespace(
    'flags',
    path = "/flags",
    description = 'Operações de permissões de usuários'
)

create_flag_model = namespace.model("create_flag", {
    "identifier": fields.String(
        description = "Identificador da flag",
        required = True),
    "description": fields.String(
        description = "Descrição da flag",
        required = True),
    "title": fields.String(
        description = "Titulo de exibição", 
        required = True)
})

@namespace.route('')
class FlagList(Resource):
    @namespace.doc('list_flags')
    def get(self):
        '''Lista todas as flags'''
        session = Session()

        # get list of flags
        flags = []
        for flag in session.query(Flag).all():
            # generate list of flag privileges
            privileges = []
            for privilege in flag.privileges:
                privileges.append(privilege.identifier)
            
            flags.append({
                "flag": dictionarize(flag),
                "privileges": privileges
            })
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": flags
        }
        return jsonify(response)
    
    @namespace.doc('create_flag')
    @namespace.expect(create_flag_model)
    def post(self):
        '''Cria uma nova flag'''
        session = Session()

        # get flag information provided in the request
        flag_data = request.get_json(force = True)

        # check if flag already exists
        flag_id = flag_data['identifier']
        flag_scalar = session.query(Flag).filter_by(identifier = flag_id).scalar()
        if flag_scalar is not None:
            response = {
                "status": 409,
                "message": "Conflict",
                "error": True,
                "response": "Flag already exists"
            }
            return jsonify(response)

        # create database model
        new_flag = Flag(
			identifier = flag_id,
			description = flag_data['description'],
			title = flag_data['title'],
		)

        if 'privileges' in flag_data:
            # get list of privileges
            req_privileges = flag_data['privileges']
            grantable = []
            for priv in req_privileges:
                # check if requested privilege exists
                item = session.query(Privilege).filter_by(identifier = priv)
                if item.scalar() is not None:
                    # check if privilege can be granted to users
                    privilege = item.one()
                    if privilege.assignable is not False:
                        grantable.append(privilege)
            
            # assign grantable privileges to flag
            new_flag.privileges = grantable

        # add new flag entity to database
        session.add(new_flag)
        session.commit()

        # generate a list of granted privilege identifiers
        granted = []
        for privilege in grantable:
            granted.append(privilege.identifier)

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": {
                "flag": dictionarize(new_flag),
                "privileges": granted
            }
        }
        return jsonify(response)

@namespace.route('/<id>')
@namespace.param('id', 'Identificador da flag')
@namespace.response(404, 'Flag não encontrado')
class SpecificFlag(Resource):
    @namespace.doc('get_flag')
    def get(self, id):
        '''Mostra uma flag específica'''
        session = Session()

        flag = session.query(Flag).filter_by(identifier = id).first()
        if flag is None:
            namespace.abort(404)
        
        # generate a list of granted privileges
        privileges = []
        for privilege in flag.privileges:
            privileges.append(privilege.identifier)
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": {
                "flag": dictionarize(flag),
                "privileges": privileges
            }
        }
        return jsonify(response)

    @namespace.doc('delete_privilege')
    def delete(self, id):
        '''Deleta uma flag'''
        session = Session()

        # look up given flag
        given_flag = session.query(Flag).filter_by(identifier = id)

        # check if given flag exists
        if given_flag.scalar() is None:
            namespace.abort(404)

        # delete flag entry from database
        flag = given_flag.one()
        records = dictionarize(flag)

        # generate a list of granted privileges
        privileges = []
        for privilege in flag.privileges:
            privileges.append(privilege.identifier)

        session.delete(flag)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": {
                "flag": records,
                "privileges": privileges
            }
        }
        return jsonify(response)

    @namespace.doc('update_flag')
    def put(self, id):
        '''Atualiza os dados de uma flag'''
        session = Session()

        # look up given flag
        given_flag = session.query(Flag).filter_by(identifier = id)

        # check if given flag exists
        if given_flag.scalar() is None:
            namespace.abort(404)

        # update flag entry with given values
        flag = given_flag.one()

        for datafield in request.args:
            if datafield.lower() != 'privileges':
                setattr(flag, datafield, request.args[datafield])

        flag = session.query(Flag).filter_by(identifier = id).one()

        if 'privileges' in request.args:
            # get list of privileges
            req_privileges = request.args['privileges'].split(",")
            grantable = []
            for priv in req_privileges:
                # check if requested privilege exists
                item = session.query(Privilege).filter_by(identifier = priv)
                if item.scalar() is not None:
                    # check if privilege can be granted to users
                    privilege = item.one()
                    if privilege.assignable is not False:
                        grantable.append(privilege)
            
            # assign grantable privileges to flag
            flag.privileges = grantable
        
        session.add(flag)
        session.commit()

        # generate a list of granted privileges
        granted = []
        for privilege in grantable:
            granted.append(privilege.identifier)

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": {
                "flag": dictionarize(flag),
                "privileges": granted
            }
        }
        return jsonify(response)
