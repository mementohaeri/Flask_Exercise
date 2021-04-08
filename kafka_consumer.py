from kafka import KafkaConsumer
import time
import json
import threading
from datetime import datetime

#import mariadb
import pymysql
import uuid

config = {
    'host': '172.19.0.3',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'mydb'
}

consumer = KafkaConsumer('new_orders',
                        bootstrap_servers=['172.19.0.101:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        auto_commit_interval_ms=1000,
                        consumer_timeout_ms=1000
                        )

conn = pymysql.connect(**config)
cursor= conn.cursor()
sql = "INSERT INTO delivery_status(delivery_id, order_json, status) VALUES (%s,%s,%s)"

def fetch_latest_orders(next_call_in):
    next_call_in += 30
    
    batch = consumer.poll(timeout_ms=100)
    if len(batch) > 0:
        for message in list(batch.values())[0]:
            value = message.value.decode()
            # order_dict = json.loads(value) #json -> dict
            # print(order_dict["ordered_at"])

            delivery_id = str(uuid.uuid4())
            status = 'CONFIRMED'
            #db insert
            cursor.execute(sql, [delivery_id,value, status])
            conn.commit()

    threading.Timer(next_call_in-time.time(),
                    fetch_latest_orders,
                    [next_call_in]).start()

next_call_in = time.time()
fetch_latest_orders(next_call_in)

