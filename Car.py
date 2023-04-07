import paho.mqtt.client as paho
import threading
from time import sleep
import random as rd
import  variables as vb
import json



class Client():
    def __init__(self, name, broker, port, battery=100 ) -> None:
        
        self.seed_rand = rd.randint(1,20) # Ao criar uma classe gera um número aleatório para por como semente
        self.id = 'car1' 
        self.broker = "localhost"
        self.port = 1883
        self.client = paho.Client(name)  # create client object
        self.client.on_publish = self.on_publish  # assign function to callback
        self.client.connect(self.broker, self.port)
        self.battery = battery  # battery level in percentage
        self.list_p = [] # lista de posições onde o carro poderá estar
        for i in range(1, 7):
            self.list_p.append(chr(64 + i))


    def on_publish(self, client, userdata, result):  # create function for callback
        print("data published \n")
    


    def decrease_battery(self, distance):
        # diminui 1% por 2km
        self.battery -= distance/200
        print(self.battery)
    
    # Envia a mensagem para o broker, informando que a bateria está baixa.
    def send_msg(self):
        self.num_stations()
        while True:
            sleep(1)  
            if self.battery < 99: 
                rd.seed(self.seed_rand) # gera o mesmo número por causa da função seed
                msg = json.dumps({"localizacao":self.random_position()}).encode()
                self.client.publish("/location",msg)

            self.decrease_battery(100)

    # Gera um número referente a posição do vertor dos vértices. Excluindo os postos
    def random_position(self):
        return rd.randint(0,len(self.list_p) - self.num_stations())

    # Retorna quantos postos existem
    def num_stations(self):
        n =0
        for p in vb.VERTICES:
            if("P" in p):
                n+=1
        return n