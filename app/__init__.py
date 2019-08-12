from flask_api import FlaskAPI
from app.init_mongodb import create_mongo
from app.init_postgres import create_postgres
from flasgger import Swagger

# local import
from instance.config import app_config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    swagger = Swagger(app)
    # http://localhost:5000/apidocs/

    create_postgres(app)
    create_mongo(app)

    return app