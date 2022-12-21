import time
import threading
from kafka import KafkaConsumer
from json import loads
import pydoop.hdfs as hdfs
import pandas as pd
import os


x_items=[]
file=1


def consumer():
    global x_items
    consumer = KafkaConsumer(
    'tshark11',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     value_deserializer=lambda x: loads(x.decode('utf-8')))
    # print('in consumer')
    try:
        for message in consumer:
            # print('consumer again')
            message1 = message.value
            # print(len(x_items),message1)
            x_items.append(message1)
    except Exception as e: print(e)
  
def file_sink():
    global x_items, file
    while True:
        time.sleep(5)
        # print('sink')
        df = pd.DataFrame(x_items)
        x_items=[]
        print(len(df))
        file_name=str(file)+'.parquet'
        df.to_parquet(file_name, engine='fastparquet')
        hdfs.put(file_name, 'hdfs://localhost:9000/python/'+file_name)
        os.remove(file_name)
        file+=1



t1 = threading.Thread(target=consumer)
t1.start()

t2 = threading.Thread(target=file_sink)
t2.start()
