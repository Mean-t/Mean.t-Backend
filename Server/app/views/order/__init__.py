from flask_restful import Api

from app.blueprints import api_v1_blueprint
from app.views.order import inquiry

api_order = Api(api_v1_blueprint, prefix='/order')

api_order.add_resource(inquiry.Order, '')
