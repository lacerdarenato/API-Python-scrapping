from model.data import alchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class NotebookModel(alchemy.Model):
    __tablename__ = 'notebook'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    productId = alchemy.Column(alchemy.Integer, unique=True)
    title = alchemy.Column(alchemy.String(50))
    price = alchemy.Column(alchemy.Float)
    description = alchemy.Column(alchemy.String(200))
    rating = alchemy.Column(alchemy.Integer)
    review = alchemy.Column(alchemy.String(40))
    #cart_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('cart.id'))

    def __init__(self, productId, title, price, description, rating, review): #cart_id
        self.productId = productId
        self.title = title
        self.price = price
        self.description = description
        self.rating = rating
        self.review = review
        #self.cart_id = cart_id
    
    def json(self):
        return {'id':self.id, "productId": self.productId, 'title':self.title, 'price':self.price, 'description':self.description, 'rating':self.rating, 'review':self.review}

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()

    @classmethod
    def find_by_product_id(cls, productId):
        return cls.query.filter_by(productId=productId).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class NotebookSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotebookModel
        include_relationships = True
        load_instance = True