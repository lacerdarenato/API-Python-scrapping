from model.data import alchemy
from . import notebook, user
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,  auto_field

class CartItemModel(alchemy.Model):
    __tablename__ = 'cart_item'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    quantity = alchemy.Column(alchemy.Integer, nullable=False)
    notebook_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('notebook.id'))
    notebooks = alchemy.relationship(notebook.NotebookModel, backref="CartItemModel")
    user_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('user.id'))
    users = alchemy.relationship(user.UserModel, backref="CartItemModel")

    def __init__(self, quantity, notebook_id, user_id):
        self.user_id = user_id
        self.notebook_id = notebook_id
        self.quantity = quantity

    def json(self):
        nbk = notebook.NotebookModel.find_by_product_id(self.notebook_id)
        return {'notebook':nbk.json(), 'quantity':self.quantity, 'user_id':self.user_id}

    def add_to_session(self):
        alchemy.session.add(self)
    
    def save_to_db(self):
        alchemy.session.commit()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class CartItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CartItemModel
        include_relationships = True
        load_instance = True
