from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields

from aedem.utils import dictionarize

from aedem.models import Session
from aedem.models.reports import Report

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
        required = False),
    "geolatitude": fields.String(
        description = "Coordenada de Latitude da denúncia",
        required = False),
    "geolongitude": fields.String(
        description = "Coordenada de Longitude da denúncia",
        required = False),
    "description": fields.String(
        description = "Descrição da denúncia",
        required = False)
})

@namespace.route('')
class ReportList(Resource):
    @namespace.doc('list_reports')
    def get(self):
        '''Listagem de todas as denúncias'''
        session = Session()

        # get list of reports
        reports = []
        for report in session.query(Report).all():
            reports.append(dictionarize(report))
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": reports
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

        # add new report to database
        session.add(new_report)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(new_report)
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
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(report)
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

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(report)
        }

        return jsonify(response)