from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields

from aedem.utils import dictionarize

from aedem.models import Session
from aedem.models.users import User
from aedem.models.replies import Reply
from aedem.models.reports import Report

namespace = Namespace(
    'replies',
    path = "/replies",
    description = 'Operações de respostas'
)

create_reply_model = namespace.model("create_reply", {
    "user": fields.String(
        description = "UUID do usuário criador da resposta",
        required = True),
    "report": fields.Integer(
        description = "ID da denúncia",
        required = True),
    "content": fields.String(
        description = "Conteúdo da resposta",
        required = True)
})

@namespace.route('')
class ReplyList(Resource):
    @namespace.doc('list_replies')
    def get(self):
        '''Listagem de todas as respostas'''
        session = Session()

        res = []
        for reply in session.query(Reply).all():
            res.append(dictionarize(reply))

        #respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": res
        }

        return jsonify(response)

    @namespace.doc('create_reply')
    @namespace.expect(create_reply_model)
    def post(self):
        '''Cria uma nova resposta'''
        session = Session()

        # get reply data provided in the request
        replydata = request.get_json(force = True)

        # create database model
        new_reply = Reply(
            content = replydata['content']
        )

        # check if given user and report exists
        user_id = replydata['user']
        given_user = session.query(User).filter_by(id = user_id)
        
        report_id = replydata['report']
        given_report = session.query(Report).filter_by(id = report_id)

        if (given_user.scalar() is None) or (given_report.scalar() is None):
            response = {
                "status": 404,
                "message": "Not Found",
                "error": True,
                "response": "User or Report not found"
            }
            return jsonify(response)

        # attach user and report to reply
        new_reply.user = given_user.one()
        new_reply.report = given_report.one()

        # add new reply to database
        session.add(new_reply)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(new_reply)
        }
        return jsonify(response)

@namespace.route('/<id>')
@namespace.param('id', 'Identificador da resposta')
@namespace.response(404, 'Reply não encontrado')
class SpecificReply(Resource):
    @namespace.doc('get_reply')
    def get(self, id):
        '''Mostra uma resposta específica'''
        session = Session()

        reply = session.query(Reply).filter_by(id = id).first()
        if reply is None:
            namespace.abort(404)

        #respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(reply)
        }

        return jsonify(response)

    @namespace.doc('delete_reply')
    def delete(self, id):
        '''Deleta uma resposta específica'''
        session = Session()

        given_reply = session.query(Reply).filter_by(id = id)

        if given_reply.scalar() is None:
            namespace.abort(404)

        # delete reply from database
        report = given_reply.one()
        records = dictionarize(report)
        session.delete(report)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": records
        }
        return jsonify(response)

    @namespace.doc('update_reply')
    def put(self, id):
        '''Altera uma resposta específica'''
        session = Session()

        given_reply = session.query(Reply).filter_by(id = id)

        if given_reply.scalar() is None:
            namespace.abort(404)

        reply = given_reply.one()

        # user and report cant be changed
        for datafield in request.args:
            if (datafield.lower() != 'user') and (datafield.lower() != 'report'):
                setattr(reply, datafield, request.args[datafield])

        session.add(reply)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(reply)
        }
        return jsonify(response)