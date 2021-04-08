# pip install flask_restful
# pip install mariadb

from flask import Flask, jsonify
import flask_restful
from flask_restful import reqparse

app = Flask(__name__)
app.config["DEBUG"] = True
api = flask_restful.Api(app)

def multiply(param1, param2):
    return param1 * param2

@app.route('/')
def index():
    return "Hello, Flask!"

class HelloWorld(flask_restful.Resource):
    def get(self):
        parser = reqparse.RequestParser()
        
        # Query String
        # GET /api/multiply?param1=3&param2=4
        parser.add_argument('param1')
        parser.add_argument('param2')
        args = parser.parse_args()
        
        param1 = args['param1']
        param2 = args['param2']

        if (not param1) or (not param2) :
            return {
                'state' : 0,
                'response' : None
            }

        param1 = int(param1)
        param2 = int(param2)

        result = multiply(param1, param2)
        return {
            'state' : 1,
            'response' : result
        }
# GET,POST,PUT,DELETE ...
# /api/multiply -> GET
# 만일 POST 메서드 사용하려면 def post 사용
# HelloWorld 클래스 안에 한꺼번에 만드는게 효율적
api.add_resource(HelloWorld, '/api/multiply')

if __name__ == '__main__':
    app.run()