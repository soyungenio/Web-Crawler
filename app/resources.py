from pathlib import Path
from urllib.parse import urljoin

from flask import request, current_app as app, send_file
from flask_restful import Resource
from marshmallow import ValidationError

from app.loader import Loader
from app.models import Sites
from app.schemas import SiteLoaderJsonSchema
from config import *

loader_thread = {}


def form_response(data=None, message=None, code=None):
    response = {}

    if data is not None:
        response = data
    elif message is not None:
        response['message'] = message

    return response, code


class SiteZipResource(Resource):
    def get(self, id):
        zip_path = os.path.join(app.root_path, "../", SITE_FOlDER, str(id), SITE_FIlENAME)
        return send_file(zip_path, as_attachment=True, attachment_filename='site.zip', mimetype='application/zip')


class SiteLoaderResource(Resource):
    def get(self, id):
        # check status of thread
        if id in loader_thread:
            if loader_thread[id].is_alive():
                return form_response(code=200, data={"status": "processing", "zip_url": ""})

        # check site folder
        zip_path = os.path.join(SITE_FOlDER, str(id), SITE_FIlENAME)
        if os.path.exists(zip_path):
            zip_url = urljoin(HOST, "api/v1/site/{}/zip".format(id))
            return form_response(code=200, data={"status": "done", "zip_url": zip_url})
        else:
            return form_response(code=400, message="Site with id={} is not found")


class SiteLoaderListResource(Resource):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return form_response(code=400, message='Invalid payload')

        # validate and deserialize input
        site_loader_schema = SiteLoaderJsonSchema()
        try:
            data = site_loader_schema.load(json_data)
        except ValidationError as err:
            return form_response(code=400, message=err.messages)

        site_url = data.get("url")

        # create record to database and get id for new site
        site = Sites(url=site_url)
        site.flush()
        site_id = site.id

        # create folder for new site
        site_path = os.path.join(SITE_FOlDER, str(site_id), SITE_FOLDER_NAME)
        Path(site_path).mkdir(parents=True, exist_ok=True)

        # set path
        site.path = site_path

        # make commit for new record
        site.save_to_db()

        # start downloading site
        loader = Loader(site_url, CRAWLER_DEPTH, site_path)
        loader.start()

        # remember thread for this downloading
        loader_thread[site_id] = loader
        return form_response(code=201, data={"site_id": site_id})
