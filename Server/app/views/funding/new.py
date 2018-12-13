from flasgger import swag_from
from flask import request

from app.extensions import db
from app.docs.sample import *
from app.views import BaseResource
from app.models import Funding


class NewFunding(BaseResource):
    @swag_from(SAMPLE_POST)
    def post(self):
        pass


class NewFundingVerify(BaseResource):
    @swag_from(SAMPLE_POST)
    def post(self):
        pass
