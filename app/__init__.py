from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

import config
from .models import db


def create_app():
    # instantiate the app
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URL
    app.config["SQLALCHEMY_POOL_RECYCLE"] = config.POOL_RECYCLE
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.TRACK_MODIFICATIONS

    # instantiate the api
    api = Api(app)

    # set up extensions
    db.init_app(app)

    # make migrations
    migrate = Migrate(app, db)

    # add resources
    from app import resources
    api.add_resource(resources.SiteLoaderListResource, '/api/v1/site')
    api.add_resource(resources.SiteLoaderResource, '/api/v1/site/<int:id>')
    api.add_resource(resources.SiteZipResource, '/api/v1/site/<int:id>/zip')

    return app
