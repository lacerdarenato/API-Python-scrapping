from flask import Flask, json, jsonify, request
from model.data import alchemy
from BotScraper import scraping

from model import notebook


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/dbNotebooks'

@app.before_first_request
def create_tables():
    alchemy.create_all()

'''evitar duplicados testar

    https://www.imaginarycloud.com/blog/flask-python/
    https://realpython.com/flask-connexion-rest-api/

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
def execute_bot():
    return scraping('Lenovo')

@app.route('/salva', methods=['GET'])
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


if __name__ == '__main__':
    from model.data import alchemy, ma
    alchemy.init_app(app)
    ma.init_app(ma)
    app.run(port=5000, debug=True),