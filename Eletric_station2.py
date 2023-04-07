import random
import time
import paho.mqtt.client as mqtt_client
import threading as td
import json


class EletricStation():
    def __init__(self, name, address, port) -> None:
        self.name = name
        self.queue = 0

        self.broker = address
        self.port = port
        self.topic = "/num_vagas"
        # generate client ID with pub prefix randomly
        #client_id = f'python-mqtt-{random.randint(0, 1000)}'
        # username = 'emqx'
        # password = 'public'
        
        self.client = mqtt_client.Client(name)
        self.client.connect(self.broker, self.port)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        td.Thread(target=self.client.loop_forever).start()
        


    def on_connect(self, client, userdata, flags, rc):

        print("Conexão estabelecida com o código de retorno: {}".format(rc))
        # Inscreve-se em um tópico
        client.subscribe("/vagas")

        
    
    def on_message(self, client, userdata, message):
        print("Mensagem recebida no tópico: {}, msg: {}  nível QoS {}".format(message.topic,
                                                                            message.payload.decode(),
                                                                            message.qos))
        if(message.topic == "/vagas"):
            print("vou mandar as minha vagas")
            msg = json.dumps({"name": self.name, "vacancy": self.queue}).encode()
            time.sleep(1)
            self.client.publish("/num_vagas", msg)



    '''def publish(self):
        msg_count = 0
        time.sleep(1)
        msg = {"name":self.name, "queue":self.queue}
        result = self.client.publish(self.topic, json.dumps(msg))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")
        msg_count += 1'''




if __name__ == '__main__':
    client = EletricStation("P2", 'localhost', 1883)
    