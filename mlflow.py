import mlflow
import time
ips=['0.0.0.0', '1.1.1.1', '2.2.2.2', '3.3.3.3']
with mlflow.start_run():
    for epoch in range(0, 500):
        mlflow.log_metric(key=ips[epoch%4], value=0.1*epoch)
