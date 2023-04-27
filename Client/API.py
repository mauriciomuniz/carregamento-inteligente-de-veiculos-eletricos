from flask import Flask, jsonify
#from Car import Client

app = Flask(__name__)


@app.route("/bateria")
def hello_world():
    return "<p>Hello, World!</p>"

'''# todos carros
@app.route("/carros")
def listar_carros():
    return jsonify([c.id for c in carros])

# bateria
@app.route("/bateria/<string:nome_carro>")
def bateria_carro(nome_carro):
    carro = next((c for c in carros if c.id == nome_carro), None)
    if carro is not None:
        return jsonify({"bateria": carro.battery})
    else:
        return jsonify({"mensagem": "Carro não encontrado"})'''


def read_file():
     pass