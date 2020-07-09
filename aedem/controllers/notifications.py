from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from aedem.utils import dictionarize
from aedem.models import Session
from aedem.models.notifications import Notification
from aedem.models.users import User

namespace = Namespace(
    'notifications',
    path = "/notifications",
    description = 'Operações de notificações'
)

create_notification_model = namespace.model("create_notification", {
    "notiftype": fields.String(
        description = "Tipo de notificação",
        required = True),
    "content": fields.String(
        description = "Conteúdo da notificação", 
        required = True)
})

@namespace.route('')
class NotificationList(Resource):
    @namespace.doc('list_notification')
    def get(self):
        '''Lista todas as notificações'''
        session = Session()

        # get list of notifications
        notifications = []
        for notification in session.query(Notification).all():
            notifications.append(dictionarize(notification))
        
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": notifications
        }
        return jsonify(response)
    
    @namespace.doc('create_notification')
    @namespace.expect(create_notification_model)
    def post(self):
        '''Cria uma nova notificação'''
        session = Session()

        # get notification information provided in the request
        notif_data = request.get_json(force = True)

        # check if given user exists
        user_id = notif_data['user_id']
        user = session.query(User).filter_by(id = user_id)
        if user.scalar() is None:
            response = {
                "status": 404,
                "message": "Not Found",
                "error": True,
                "response": "User has not been found"
            }
            return jsonify(response)

        # create database model
        new_notification = Notification(
			content = notif_data['content'],
			notiftype = notif_data['notiftype'])
        
        new_notification.user = user.one()

        # add new notification entity to database
        session.add(new_notification)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(new_notification)
        }
        return jsonify(response)

@namespace.route('/<id>')
@namespace.param('id', 'Identificador da notificação')
@namespace.response(404, 'Notificação não encontrado')
class SpecificNotification(Resource):
    @namespace.doc('get_notification')
    def get(self, id):
        '''Mostra uma notificação específica'''
        session = Session()

        notification = session.query(Notification).filter_by(id = id).first()
        if notification is None:
            namespace.abort(404)
    
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(notification)
        }
        return jsonify(response)

    @namespace.doc('delete_notification')
    def delete(self, id):
        '''Deleta uma notificação'''
        session = Session()

        # look up given flag
        given_notification = session.query(Notification).filter_by(id = id)

        # check if given notification exists
        if given_notification.scalar() is None:
            namespace.abort(404)

        # delete notification entry from database
        notification = given_notification.one()
        records = dictionarize(notification)

        session.delete(notification)
        session.commit()

        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": records
        }
        return jsonify(response)

    @namespace.doc('update_notification')
    def put(self, id):
        '''Atualiza os dados de uma notificação'''
        session = Session()

        # look up given flag
        given_notification = session.query(Notification).filter_by(id = id)

        # check if given notification exists
        if given_notification.scalar() is None:
            namespace.abort(404)

        # update notification entry with given values
        notification = given_notification.one()

        for datafield in request.args:
            if datafield != 'user_id':
                setattr(notification, datafield, request.args[datafield])

        if 'user_id' in request.args:
            # check if given user exists
            user = session.query(User).filter_by(id = request.args['user_id'])
            if user.scalar() is None:
                response = {
                    "status": 404,
                    "message": "Not Found",
                    "error": True,
                    "response": "User has not been found"
                }
                return jsonify(response)
            
            notification.user = user.one()

        session.add(notification)
        session.commit()
    
        # respond request
        response = {
            "status": 200,
            "message": "Success",
            "error": False,
            "response": dictionarize(notification)
        }
        return jsonify(response)
