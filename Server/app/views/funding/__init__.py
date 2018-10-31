from flask_restful import Api

from app.blueprints import api_v1_blueprint
from app.views.funding import manage

api_funding = Api(api_v1_blueprint, prefix='/funding/patron')

api_funding.add_resource(manage.Patron, '/')
