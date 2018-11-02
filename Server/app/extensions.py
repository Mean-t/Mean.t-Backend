from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_validation import Validator
from flasgger import Swagger

cors: CORS = CORS()
jwt: JWTManager = JWTManager()
validator: Validator = Validator()
swagger: Swagger = Swagger()
db: SQLAlchemy = SQLAlchemy()
