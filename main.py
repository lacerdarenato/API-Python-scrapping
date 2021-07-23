from flask import Flask, json, jsonify

app = Flask(__name__)

with open('dados.json', 'r') as myfile:
    data=myfile.read()

objectsNotebooks = json.loads(data)

@app.route('/getall',methods=['GET'])
def getNotebooks():
    return jsonify(objectsNotebooks)
@app.route('/todo/create',methods=['POST'])
def createNotebooks():
    return 'Create new notebook'