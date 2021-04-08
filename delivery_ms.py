import flask
from flask import Flask, jsonify, request
from flask_restful import reqparse
from datetime import datetime

import flask_restful
#import mariadb
import pymysql
import json
import uuid

app = Flask(__name__)
app.config["DEBUG"] = True
api = flask_restful.Api(app)

config = {
    'host': '172.19.0.3',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'mydb'
}

@app.route('/')
def index():
    return "Welcome to DELIVERY Microservice!"

class Delivery(flask_restful.Resource):
    def __init__(self):
        self.conn = pymysql.connect(**config)
        self.cursor = self.conn.cursor()

    def get(self):
        sql = "select delivery_id, order_json, status, created_at from delivery_status order by id desc"
        self.cursor.execute(sql)
        result_set = self.cursor.fetchall()
        
        row_headers = [x[0] for x in self.cursor.description]
        
        json_data = []
        for result in result_set:
            json_data.append(dict(zip(row_headers, result)))

        return jsonify(json_data)

# {"status" : "COMPLETED"}
class DeliveryStatus(flask_restful.Resource):
    def __init__(self):
        self.conn = pymysql.connect(**config)
        self.cursor = self.conn.cursor()

    def put(self,delivery_id):
        json_data = request.get_json()
        status = json_data['status']

        sql = "UPDATE delivery_status SET status = %s WHERE delivery_id=%s"

        self.cursor.execute(sql,[status, delivery_id])
        self.conn.commit()

        json_data['updated_at'] = str(datetime.today())
        response = jsonify(json_data)
        response.status_code = 201

        return response

api.add_resource(Delivery, '/delivery-ms/deliveries')
api.add_resource(DeliveryStatus,'/delivery-ms/deliveries/<string:delivery_id>')

if __name__ == '__main__':
    app.run(port=6000)