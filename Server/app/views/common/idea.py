from flasgger import swag_from
from flask import request

from app.docs.sample import *
from app.views import BaseResource


class IdeaMain(BaseResource):
    @swag_from(SAMPLE_POST)
    def post(self):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)


class IdeaSearch(BaseResource):
    @swag_from(SAMPLE_POST)
    def get(self, index):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)


class IdeaInstance(BaseResource):
    @swag_from(SAMPLE_POST)
    def get(self, index):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)

    def delete(self, index):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)

    def patch(self, index):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)