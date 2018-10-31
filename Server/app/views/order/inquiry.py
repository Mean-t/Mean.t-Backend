from flasgger import swag_from
from flask import request

from app.docs.sample import *
from app.views import BaseResource


class Order(BaseResource):
    @swag_from(SAMPLE_POST)
    def post(self, code):
        payload = request.json

        if not payload['age']:
            raise self.ValidationError('Age is 0!')

        return self.unicode_safe_json_dumps(payload, 201)
