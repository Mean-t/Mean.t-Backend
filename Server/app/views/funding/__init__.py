from flask_restful import Api

from app.blueprints import api_v1_blueprint
from app.views.funding import manage

api_patron = Api(api_v1_blueprint, prefix='/funding/patron')

api_patron.add_resource(manage.Patron, '')
