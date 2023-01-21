from kafka import KafkaConsumer
import pydoop.hdfs as hdfs
from json import loads

consumer = KafkaConsumer(
    'test',
     bootstrap_servers=['192.168.18.29:9092'],
     auto_offset_reset="latest",
     enable_auto_commit=False,
     value_deserializer=lambda x: loads(x.decode('utf-8')))
hdfs_path = 'hdfs://0.0.0.0:9000/test2/file.json'


print(hdfs.ls('/'))



for message in consumer:
   message = message.value
   with hdfs.open(hdfs_path, 'at') as f:
       print(message)
       f.write(f"{message}\n")
