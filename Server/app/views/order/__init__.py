from flask_restful import Api

from app.blueprints import api_v1_blueprint
from app.views.order import inquiry

api_funding = Api(api_v1_blueprint, prefix='/funding')

api_funding.add_resource(inquiry.Order, '/')
