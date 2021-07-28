from data import alchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema 

class UserModel(alchemy.Model):
    __tablename__ = 'user'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    username = alchemy.Column(alchemy.String(50), unique=True)
    email = alchemy.Column(alchemy.String(50), unique=True)
    password = alchemy.Column(alchemy.String(50))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    def json(self):
        return {'username': self.username, 'email': self.email, 'password': self.password}
    
    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()
    
    def delete_to_db(self):
        alchemy.session.delete(self)
        alchemy.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = True
        load_instance = True