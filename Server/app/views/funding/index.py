from flasgger import swag_from
from flask import request

from app.extensions import db
from app.docs.sample import *
from app.views import BaseResource
from app.models import Funding


class FundingIndex(BaseResource):
    @swag_from(SAMPLE_POST)
    def get(self):
        query_string = dict(request.query_string)
        fundings = Funding.query.filter_by(**query_string).all()

        return self.unicode_safe_json_dumps([
            {'id': funding.funding_id,
             'title': funding.title,
             'expiration': funding.expiration,
             'title_img': funding.title_img_path}
            for funding in fundings
        ])
