from model.data import alchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,  auto_field

from . import notebook, user

class CartModel(alchemy.Model):
    __tablename__ = 'cart'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    quantity = alchemy.Column(alchemy.Integer, nullable=False)
    #user_id = alchemy.relationship(user.UserModel, lazy='dynamic')
    #notebook_id = alchemy.relationship(notebook.NotebookModel, lazy='dynamic')

    def __init__(self, quantity, notebook_id):
        self.quantity = quantity
        #self.notebook_id = notebook_id

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()
    
    def json(self):
        return {'notebook_id':self.notebook_id, 'quantity': self.quantity}

    @classmethod
    def find_by_notebook(cls, notebook_id):
        return cls.query.filter_by(notebook_id=notebook_id).first()

    '''@classmethod
    def find_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()'''
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    
class CartSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CartModel
        include_relationships = True
        load_instance = True