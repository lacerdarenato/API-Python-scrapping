from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

alchemy = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()