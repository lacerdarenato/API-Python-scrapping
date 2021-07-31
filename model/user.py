from model.data import alchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class UserModel(alchemy.Model):
    __tablename__ = 'user'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String(100), nullable=False)
    email = alchemy.Column(alchemy.String(100), nullable=False, unique=True)
    password = alchemy.Column(alchemy.String(110), nullable=False)
    
    #cart_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('cart.id'))

    def __init__(self, name, email, password, cart_id): 
        self.name = name
        self.email = email
        self.password = password
        self.cart_id = cart_id 
    
    def json(self):
        return {'name': self.name, 'email': self.email, 'password': self.password}
    
    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()
    
    def delete_to_db(self):
        alchemy.session.delete(self)
        alchemy.session.commit()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = True
        load_instance = True