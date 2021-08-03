from flask import Flask, json, jsonify, request
from model.data import alchemy
from BotScraper import scraping
from model import notebook, user, cart_item
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from validate_email import validate_email
from datetime import timedelta
#from flask_restx import Api

app = Flask(__name__)
'''api = Api(  app, 
            version='1.0',
            title='Api de notebooks', 
            description='Apenas uma api com scraping de dados de notebooks', 
            doc='/docs'
        )'''


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/dbNotebooks'
app.config['JWT_SECRET_KEY'] = 'YMujEXUERyR9Zgixpa6iEDFfypQ'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=600)


@app.before_first_request
def create_tables():
    alchemy.create_all()

def open_json():
    try: 
        json_file = open('dados.json', 'r')
        data = json_file.read()
        json_file.close()
        objectsNotebooks = json.loads(data)
        return objectsNotebooks
    except OSError as err:
        print("OS Error: {0}".format(err))
        return "Erro ao carregar arquivo json", 404

@app.route('/', methods=['GET'])
def home():
    return "API Funcionando", 200

@app.route('/notebook',methods=['GET'])
@jwt_required()
def get_notebooks():
    return jsonify(open_json())

@app.route('/notebook/<int:productId>', methods=['GET'])
@jwt_required()
def get_notebook_by_product_id(productId):
    result = notebook.NotebookModel.find_by_product_id(productId)
    if result:
        return result.json()
    return {'message':'Notebook não encotrado'}, 404

@app.route('/notebook/<int:productId>', methods=['DELETE'])
@jwt_required()
def del_notebook_by_product_id(productId):
    result = notebook.NotebookModel.find_by_product_id(productId)
    if result:
        notebook.NotebookModel.remove_from_db(result)
        return {'message':'Notebook removido com sucesso'}, 200
    return {'message':'Notebook não encotrado'}, 404

@app.route('/notebook/<int:productId>', methods=['PATCH'])
@jwt_required()
def change_notebook_by_product_id(productId):
    result = notebook.NotebookModel.find_by_product_id(productId)
    if result:
        request_data = request.get_json()
        notebook.NotebookModel.update_item(request_data)
        return request_data, 200
    return {'message':'Notebook não encotrado'}, 404

@app.route('/scrap')
@jwt_required()
def execute_bot():
    return scraping('Lenovo')

def persist_json():
    json = open_json()
    
    for notebookItem in json:
        if notebook.NotebookModel.find_by_product_id(productId=notebookItem['productId']):
            print('Item {} já existe no banco!'.format(notebookItem['productId']))
            
        else:
            newNotebook = notebook.NotebookModel(   productId=notebookItem['productId'],
                                                    title=notebookItem['title'],
                                                    price=notebookItem['price'],
                                                    description=notebookItem['description'],
                                                    rating=notebookItem['rating'],
                                                    review=notebookItem['review'])
            newNotebook.save_to_db()

    return {"message":"Json do scraping salvo no banco"}, 200

@app.route('/notebook/comprar', methods=['POST'])
@jwt_required()
def create_notebook_list_in_cart():
    request_data = request.get_json()
    notebook_list = request_data['list_to_buy']

    for item in notebook_list:
        found = notebook.NotebookModel.find_by_product_id(item['notebook_id'])
        if found:
            new_cart = cart_item.CartItemModel(quantity=item['quantity'],
                                                    notebook_id=found.id,
                                                    user_id=request_data['user_id'])
            new_cart.add_to_session()
        else:
            return {'message': 'Notebook {} nao existe no banco!'.format(item['notebook_id'])}, 403

    new_cart.save_to_db()

    return {'message': 'Notebooks inseridos com sucesso!'}, 200

@app.route('/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    name = request_data['name']
    email = request_data['email']
    password = request_data['password']
    if validate_email(email):
        if user.UserModel.find_by_email(email):
            return {'message':'Email ja cadastrado'}, 200
        else:
            new_user = user.UserModel(name, email, generate_password_hash(password))
            new_user.save_to_db()
            return jsonify(new_user.json())
    else:
        return {'message':'Email invalido'}, 401

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    result = user.UserModel.find_by_email(email)
    if result and check_password_hash(result.password, password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)

    return {"message":"Usuario ou senha invalidos"}, 401

if __name__ == '__main__':
    from model.data import alchemy, ma, jwt
    alchemy.init_app(app)
    ma.init_app(ma)
    jwt.init_app(app)
    app.run(port=5000, debug=True)