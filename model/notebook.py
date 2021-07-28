from model.data import alchemy

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class NotebookModel(alchemy.Model):
    __tablename__ = 'Notebook'

    id = alchemy.Column(alchemy.Integer, primary_key= True)
    title = alchemy.Column(alchemy.String(50))
    price = alchemy.Column(alchemy.Float)
    description = alchemy.Column(alchemy.String(200))
    rating = alchemy.Column(alchemy.Integer)
    review = alchemy.Column(alchemy.String(20))

    def __init__(self, title, price, description, rating, review):
        self.title = title
        self.price = price
        self.description = description
        self.rating = rating
        self.review = review
    
    def json(self):
        return {'id':self.id, 'title':self.title, 'price':self.price, 'description':self.description, 'rating':self.rating, 'review':self.review}

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class NotebookSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotebookModel
        include_relationships = True
        load_instance = True