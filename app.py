from flask import Flask, json, jsonify, request
from model.data import alchemy

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
def openJson():
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
def getNotebooks():
    return jsonify(openJson())

@app.route('/salva', methods=['GET'])
def persistJson():
    json = openJson()
    #print(type(json))
    
    for notebookitem in json:
        newNotebook = notebook.NotebookModel(title=notebookitem['title'],
                                            price=notebookitem['price'],
                                            description=notebookitem['description'],
                                            rating=notebookitem['rating'],
                                            review=notebookitem['review'])
        #print(type(notebookitem))
        newNotebook.save_to_db()
        if newNotebook.title in json: #como achar um dict dentro de uma lista????
            print('encontrou')

    return "Json do scraping salvo"


if __name__ == '__main__':
    from model.data import alchemy, ma
    alchemy.init_app(app)
    ma.init_app(ma)
    app.run(port=5000, debug=True),