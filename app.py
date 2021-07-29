from os import access, name
from flask import Flask, json, jsonify, request
from model.data import alchemy
from BotScraper import scraping
from model import notebook, user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from validate_email import validate_email
from datetime import timedelta

app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/dbNotebooks'
app.config['JWT_SECRET_KEY'] = 'YMujEXUERyR9Zgixpa6iEDFfypQ'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)

@app.before_first_request
def create_tables():
    alchemy.create_all()

'''evitar duplicados testar
    $query = "INSERT INTO usuarios(login, senha) 
    SELECT '$login_que_nao_pode_duplicar', 123456 
    FROM DUAL
    WHERE NOT EXISTS(SELECT login FROM usuarios WHERE login = '$valor_que_nao_pode_duplicar')";
'''
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
    return "Bem vindo a API de notebooks com Web Scraping", 200

@app.route('/listar',methods=['GET'])
def get_notebooks():
    return jsonify(open_json())

@app.route('/listar/<int:id>')
def get_notebook_by_id(id):
    result = notebook.NotebookModel.find_by_id(id)
    if result:
        return result.json()
    return {'message':'Notebook não encotrado'}, 404

@app.route('/scrap')
@jwt_required()
def execute_bot():
    return scraping('Lenovo')

@app.route('/salva', methods=['GET'])
@jwt_required()
def persist_json():
    json = open_json()
    
    for notebookitem in json:
        newNotebook = notebook.NotebookModel(title=notebookitem['title'],
                                            price=notebookitem['price'],
                                            description=notebookitem['description'],
                                            rating=notebookitem['rating'],
                                            review=notebookitem['review'])
        #print(type(notebookitem))
        newNotebook.save_to_db()

    return "Json do scraping salvo"

@app.route('/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    name = request_data['name']
    email = request_data['email']
    password = request_data['password']
    if validate_email(email):
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