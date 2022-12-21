from scapy.all import *
from kafka import KafkaProducer
from json import dumps

producer = KafkaProducer(bootstrap_servers='localhost:9092', linger_ms=10, 
            value_serializer=lambda v:dumps(v).encode('utf-8')
)

def handler(x):
    packet={}
    if(x.haslayer(TCP)):
        packet['tcp_window']=x[TCP].window
        packet['payload']=len(x[TCP].payload)
        packet['data_ofs']=x[TCP].dataofs
    
    if(x.haslayer(IP)):
        packet['src']=x[IP].src
        packet['dst']=x[IP].dst
        packet['length']=x[IP].len
        packet['header_len']=x[IP].ihl
                
    
    
    if len(packet):
        print(packet)
        producer.send('tshark11', packet)
        producer.flush()
sniff(count=5000, prn=handler)

