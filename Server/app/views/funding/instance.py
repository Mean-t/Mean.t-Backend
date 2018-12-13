from flasgger import swag_from
from flask import request

from app.extensions import db
from app.docs.sample import *
from app.views import BaseResource
from app.models import Funding


class FundingInstance(BaseResource):
    @swag_from(SAMPLE_POST)
    def get(self, funding_id: int):
        fundings = Funding.query.filter_by(funding_id=funding_id).all()

        return self.unicode_safe_json_dumps(fundings)

    @swag_from(SAMPLE_POST)
    def patch(self, funding_id: int):
        pass

    @swag_from(SAMPLE_POST)
    def delete(self, funding_id: int):
        pass
