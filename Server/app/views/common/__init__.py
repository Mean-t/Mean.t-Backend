from flask_restful import Api

from app.blueprints import api_v1_blueprint
from app.views.common import funding, idea

api_funding = Api(api_v1_blueprint, prefix='/funding')

api_funding.add_resource(funding.FundingMain, '/')
api_funding.add_resource(funding.FundingInstance, '/<index>')
api_funding.add_resource(funding.FundingSearch, '/search')

api_idea = Api(api_v1_blueprint, prefix='/idea')

api_idea.add_resource(idea.IdeaMain, '/')
api_idea.add_resource(idea.IdeaInstance, '/<index>')
api_idea.add_resource(idea.IdeaSearch, '/search')