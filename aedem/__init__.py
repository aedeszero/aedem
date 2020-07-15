from flask import Flask, Blueprint, url_for, current_app
from flask_restplus import Api

def create_app() -> Flask:
    app = Flask(__name__)
    app.app_context().push()

    # set up config from object
    if app.config["ENV"] == "production":
        app.config.from_object("config.production.Config")
    elif app.config["ENV"] == "testing":
        app.config.from_object("config.testing.Config")
    else:
        app.config.from_object("config.development.Config")

    # ensure all database tables are created
    from aedem.models import initialize_database, engine
    from aedem.models.privileges import Privilege
    from aedem.models.flags import Flag
    from aedem.models.users import User
    from aedem.models.reports import Report
    from aedem.models.attachments import Attachment
    from aedem.models.notifications import Notification
    from aedem.models.replies import Reply
    initialize_database(engine)
    
    # create Flask blueprint
    blueprint = Blueprint(
        'api',
        __name__,
        url_prefix = app.config['BASE_URL']
    )

    # set up flask-restplus API
    api = Api(
        blueprint,
        title = app.config["APP_NAME"],
        version = app.config["APP_VERSION"],
        description = app.config["APP_DESCRIPTION"],
        doc = app.config['DOCS_RESOURCE']
    )

    # register controllers
    from aedem.controllers.users import namespace as usercontroller
    from aedem.controllers.privileges import namespace as privilegecontroller
    from aedem.controllers.flags import namespace as flagcontroller
    from aedem.controllers.reports import namespace as reportcontroller
    from aedem.controllers.notifications import namespace as notifcontroller
    api.add_namespace(usercontroller)
    api.add_namespace(privilegecontroller)
    api.add_namespace(flagcontroller)
    api.add_namespace(reportcontroller)
    api.add_namespace(notifcontroller)

    # register blueprint
    app.register_blueprint(blueprint)

    app.run(debug = app.config['DEBUG'])
    return app