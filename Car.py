import paho.mqtt.client as paho
import threading
from time import sleep

class Client():
    def __init__(self, name, broker, port, battery) -> None:
        self.broker = "localhost"
        self.port = 1883
        self.client = paho.Client(name)  # create client object
        self.client.on_publish = self.on_publish  # assign function to callback
        self.client.connect(self.broker, self.port)
        self.battery = battery  # battery level in percentage


    def on_publish(self, client, userdata, result):  # create function for callback
        print("data published \n")
    
    def decrease_battery(self, distance):
        # diminui 1% por 2km
        self.battery -= distance/200
        
    # def send_msg(self):
    #     while(True):
    #         sleep(5)
    #         self.client.publish("/topico", "Bateria baixa")
    
    def send_msg(self):
        while True:
            sleep(1)  
            # battery = self.get_battery()
            if self.battery < 99:
                self.client.publish("/topico", "bateria baixa")
            
            self.decrease_battery(10)

