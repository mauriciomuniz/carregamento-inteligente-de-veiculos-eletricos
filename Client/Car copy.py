
import sys
sys.path.insert(1, '../')

import paho.mqtt.client as paho
import threading
from time import sleep
import random as rd
import variables as vb
import json



class Client():
    def __init__(self, name, broker, port, battery=100 ) -> None:
        self.id = name
        self.client = paho.Client(name)  # create client object
        
        self.client.connect(broker, port)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish  # assign function to callback
        self.client.on_message =self.on_message
        
        self.msg = None
        self.battery = battery  # battery level in percentage
        self.list_p = [] # lista de posições onde o carro poderá estar
        for i in range(1, 7):
            self.list_p.append(chr(64 + i))

        threading.Thread(target=self.send_msg).start()
        threading.Thread(target=self.client.loop_forever).start()
        
    def wait_charge(self):
        print("Esperando carregar...")
        while True:
            pass
        
    def on_publish(self, client, userdata, result):  # create function for callback
        print("data published \n")
    
     
    # Define a função de callback que será chamada
    # quando a conexão for estabelecida
    def on_connect(self, client, userdata, flags, rc):
        print("Conexão estabelecida com o código de retorno: {}".format(rc))

        # Inscreve-se em um tópico
        self.client.subscribe(f'/{self.id}')    
    
    # Define a função de callback que será chamada quando uma mensagem for recebida
    def on_message(self, client, userdata, message):
        print("Mensagem recebida no tópico: {}, msg: {}  nível QoS {}".format(message.topic,
                                                                            message.payload.decode(),
                                                                            message.qos))
        self.msg = message
        sleep(5)   
        self.battery = 100
        threading.Thread(target=self.send_msg).start()
        
    def decrease_battery(self, distance):
        # diminui 1% por 2km
        self.battery -= distance/200
        print(self.battery)
        
    
    # Envia a mensagem para o broker, informando que a bateria está baixa.
    def send_msg(self):
        while True:
            sleep(1)  
            if self.battery < 99: 
                seed_rand = rd.randint(1,20) # Ao criar uma classe gera um número aleatório para por como semente da função seed
                rd.seed(seed_rand) # gera o mesmo número por causa da função seed
                msg = json.dumps({"localizacao":self.random_position(), "id_car":self.id}).encode()
                result = self.client.publish("/location", msg, qos=1)
                if(result[0] == 0):
                    #threading.Thread(target=self.wait_charge).start()
                    break
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
    

Client('car1', 'localhost', 1883)