from flask_restful import Api

from app.blueprints import api_v1_blueprint
from app.views.funding import instance, index, new

api_funding = Api(api_v1_blueprint, prefix='/funding')

api_funding.add_resource(index.FundingIndex, '')
api_funding.add_resource(instance.FundingInstance, '/<int:index>')
api_funding.add_resource(new.NewFunding, '/new')
api_funding.add_resource(new.NewFundingVerify, '/new/verify')
