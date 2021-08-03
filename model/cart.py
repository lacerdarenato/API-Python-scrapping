from model.data import alchemy
from . import user
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,  auto_field



class CartModel(alchemy.Model):
    __tablename__ = 'cart'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    user_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('user.id'))
    users = alchemy.relationship(user.UserModel, backref="CartItemModel")

    def __init__(self):
        self

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()
    
    def json(self):
        return {'quantity': self.id}
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
class CartSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CartModel
        include_relationships = True
        load_instance = True