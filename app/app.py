from flask import Flask, json, jsonify
from flask.wrappers import Response, Request
from flask_sqlalchemy import SQLAlchemy

import mysql.connector


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/dbNotebooks'

db = SQLAlchemy(app)

class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    price = db.Column(db.Float)
    description = db.Column(db.String(200))
    title = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    review = db.Column(db.String(20))

'''evitar duplicados testar
    $query = "INSERT INTO usuarios(login, senha) 
    SELECT '$login_que_nao_pode_duplicar', 123456 
    FROM DUAL
    WHERE NOT EXISTS(SELECT login FROM usuarios WHERE login = '$valor_que_nao_pode_duplicar')";
'''
def openJson():
    try: 
        json_file = open('dados.json', 'r')
    except OSError as err:
        print("OS Error: {0}".format(err))
    else:     
        data = json_file.read()
        json_file.close()

    objectsNotebooks = json.loads(data)

    return objectsNotebooks



@app.route('/getall',methods=['GET'])
def getNotebooks():
    return jsonify(openJson())


@app.route('/create',methods=['GET'])
def createNotebooks():
    body = openJson()

    for notebook in body:
        try: 
            notebookItem = Notebook(price=notebook["Price"],
                                     description=notebook["Description"],
                                     title=notebook["Title"],
                                     review=notebook["Review"])
            #print(notebookItem.query.filter_by(price=notebook["Price"]).first())         
            db.session.add(notebookItem)
            db.session.commit()
        except Exception as e:
            print('Erro ao inserir no banco', e)
    #print(body.query.filter_by(price=notebook["Price"]))
    return "Banco Populado"

app.run()