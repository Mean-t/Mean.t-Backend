from flasgger import swag_from
from flask import request

from app.docs.sample import *
from app.views import BaseResource


class FundingMain(BaseResource):
    @swag_from(SAMPLE_POST)
    def get(self):
        return self.unicode_safe_json_dumps("hello!", 201)

    @swag_from(SAMPLE_POST)
    def post(self):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)


class FundingSearch(BaseResource):
    @swag_from(SAMPLE_POST)
    def get(self, index):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)


class FundingInstance(BaseResource):
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

    def put(self, index):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)