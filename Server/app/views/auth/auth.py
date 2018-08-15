from flasgger import swag_from
from flask import request
from flask_restful import Api

from app import api_v1_blueprint
from app.docs.sample import *
from app.views import BaseResource

api = Api(api_v1_blueprint)


@api.resource('/auth')
class Sample(BaseResource):
    @swag_from(SAMPLE_POST)
    def post(self):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)


@api.resource('/refresh')
class Sample(BaseResource):
    @swag_from(SAMPLE_POST)
    def post(self):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)
