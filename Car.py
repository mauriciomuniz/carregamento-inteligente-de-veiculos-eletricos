import paho.mqtt.client as paho
import threading
from time import sleep

class Client():
    def __init__(self, name, broker, port) -> None:
        self.broker = "localhost"
        self.port = 1883
        self.client = paho.Client(name)  # create client object
        self.client.on_publish = self.on_publish  # assign function to callback
        self.client.connect(self.broker, self.port)


    def on_publish(self, client, userdata, result):  # create function for callback
        print("data published \n")
    
    
    def send_msg(self):
        while(True):
            sleep(5)
            self.client.publish("/topico", "Bateria baixa")

