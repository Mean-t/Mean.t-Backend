from flasgger import swag_from
from flask import request
from flask_restful import Api

from app import api_v1_blueprint
from app.docs.sample import *
from app.views import BaseResource

api = Api(api_v1_blueprint)
api.prefix = '/account/<id>'


@api.resource('/')
class Sample(BaseResource):
    @swag_from(SAMPLE_POST)
    def get(self, id):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)

    @swag_from(SAMPLE_POST)
    def patch(self, id):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)


@api.resource('/funding')
class Sample(BaseResource):
    @swag_from(SAMPLE_POST)
    def get(self, id):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)


@api.resource('/funding/<index>')
class Sample(BaseResource):
    @swag_from(SAMPLE_POST)
    def get(self, id, index):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)

    @swag_from(SAMPLE_POST)
    def patch(self, id, index):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)

