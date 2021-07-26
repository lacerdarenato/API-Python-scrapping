from flask import Flask, json, jsonify

app = Flask(__name__)

try: 
    json_file = open('dados.json', 'r')
except OSError as err:
    print("OS Error: {0}".format(err))
else:     
    data = json_file.read()
    json_file.close()

objectsNotebooks = json.loads(data)

@app.route('/getall',methods=['GET'])
def getNotebooks():
    return jsonify(objectsNotebooks)
@app.route('/create',methods=['POST'])
def createNotebooks():
    return 'Create new notebook'