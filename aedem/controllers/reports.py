from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields

from aedem.utils import dictionarize

from aedem.models import Session
from aedem.models.users import User
from aedem.models.reports import Report
from aedem.models.attachments import Attachment

namespace = Namespace(
    'reports',
    path = "/reports",
    description = 'Operações de denúncias'
)

create_report_model = namespace.model("create_report", {
    "state_abbr": fields.String(
        description = "Abreviação do Estado da denúncia",
        required = True),
    "city_name": fields.String(
        description = "Nome da Cidade da denúncia",
        required = True),
    "area": fields.String(
        description = "Bairro da denúncia",
        required = True),
    "geolatitude": fields.String(
        description = "Coordenada de Latitude da denúncia",
        required = True),
    "geolongitude": fields.String(
        description = "Coordenada de Longitude da denúncia",
        required = True),
    "description": fields.String(
        description = "Descrição da denúncia",
        required = True),
    "user": fields.String(
        description = "UUID do usuário criador da denúncia",
        required = True),
    "attachments": fields.String(
        description = "Lista de links das imagens da denúncia",
        required = True)
})

@namespace.route('')
class ReportList(Resource):
    @namespace.doc('list_reports')
    def get(self):
        '''Listagem de todas as denúncias'''
        session = Session()

        # get list of reports
        res = []
        for report in session.query(Report).all():
            attachs = []
            for attach in report.attachments:
                attachs.append(dictionarize(attach))
            
            resp = {
                "report": dictionarize(report),
                "attachments": attachs
            }
            res.append(resp)

        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": res
        }
        return jsonify(response)

    @namespace.doc('create_report')
    @namespace.expect(create_report_model)
    def post(self):
        '''Cria uma nova denúncia'''
        session = Session()

        # get report data provided in the request
        reportdata = request.get_json(force = True)

        # create database model
        new_report = Report(
            state_abbr = reportdata['state_abbr'],
            city_name = reportdata['city_name'],
            area = reportdata['area'],
            geolatitude = reportdata['geolatitude'],
            geolongitude = reportdata['geolongitude'],
            description = reportdata['description']
        )

        # check if given user exists
        user_id = reportdata['user']
        given_user = session.query(User).filter_by(id = user_id)

        if given_user.scalar() is None:
            response = {
                "status": 404,
                "message": "Not Found",
                "error": True,
                "response": "User not found"
            }
            return jsonify(response)
        
        # create and attach attachments
        for attachment in reportdata['attachments']:
            attach = Attachment(
                attachment_addr = attachment
            )
            attach.report = new_report
            attach.user = given_user.one()
            session.add(attach)

        # attach given user
        new_report.user = given_user.one()

        # add new report to database
        session.add(new_report)
        session.commit()

        attachs = []

        for item in new_report.attachments:
            attachs.append(dictionarize(item))

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": {
                "report": dictionarize(new_report),
                "attachments": attachs
            }
        }
        return jsonify(response)

@namespace.route('/<id>')
@namespace.param('id', 'Identificador da denúncia')
@namespace.response(404, 'Denúncia não encontrada')
class SpecificReport(Resource):
    @namespace.doc('get_report')
    def get(self, id):
        '''Mostrar uma denúncia específica'''
        session = Session()

        report = session.query(Report).filter_by(id = id).first()
        if report is None:
            namespace.abort(404)

        attachs = []

        for item in report.attachments:
            attachs.append(dictionarize(item))
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": {
                "report": dictionarize(report),
                "attachments": attachs
            }
        }
        return jsonify(response)

    @namespace.doc('delete_report')
    def delete(self, id):
        '''Deleta uma denúncia existente'''
        session = Session()

        # look up given report
        given_report = session.query(Report).filter_by(id = id)

        # check if given report exists
        if given_report.scalar() is None:
            namespace.abort(404)

        # delete report from database
        report = given_report.one()
        # delete the attachments of the report
        attachs = []
        for attach in report.attachments:
            attachs.append(dictionarize(attach))
            session.delete(attach)
        records = dictionarize(report)
        session.delete(report)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": {
                "report": records,
                "attachments": attachs
            }
        }
        return jsonify(response)

    @namespace.doc('update_report')
    def put(self, id):
        '''Atualiza os dados de uma denúncia'''
        session = Session()

        # look up given report
        given_report = session.query(Report).filter_by(id = id)

        # check if given report exists
        if given_report.scalar() is None:
            namespace.abort(404)

        # update report data with given values
        report = given_report.one()

        for datafield in request.args:
            setattr(report, datafield, request.args[datafield])

        session.add(report)
        session.commit()

        attachs = []

        for item in report.attachments:
            attachs.append(dictionarize(item))

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": {
                "report": dictionarize(report),
                "attachments": attachs
            }
        }

        return jsonify(response)