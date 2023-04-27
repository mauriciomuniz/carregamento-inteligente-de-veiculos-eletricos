from flask import Flask, jsonify
#from Car import Client
import file


app = Flask(__name__)


@app.route("/car1")
def hello_world():
    return read_file()


def read_file():
   return file.read("./data.json")

if __name__ == '__main__':
    app.run()
    