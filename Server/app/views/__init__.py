import json
import datetime

from flask import Response
from flask_restful import Resource


class BaseResource(Resource):
    def __init__(self):
        self.now = datetime.datetime.now()

    @classmethod
    def unicode_safe_json_dumps(cls, data=None, status_code: int=200, **kwargs) -> Response:
        return Response(
            json.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )

    class ValidationError(Exception):
        def __init__(self, description='', *args):
            self.description = description

            super(BaseResource.ValidationError, self).__init__(*args)
