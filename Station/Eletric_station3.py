import random
import time
import paho.mqtt.client as mqtt_client
import threading as td
import json

'''
    A classe EletricStation representa um posto de carregamento de veiculos elétricos
    usa o mqtt para comunicação com outras entidades e inicia com alguns atributos como nome, vagas, portas
    entre outros thread para que o cliente rode em segundo plano, enquanto outras tarefas sao executadas
'''
class EletricStation():
    def __init__(self, name, address, port, vacancy) -> None:
        self.name = name
        self.queue = vacancy
       
        self.broker = address
        self.port = port
        self.topic = "/num_vagas3"
        
        self.client = mqtt_client.Client(name)
        self.client.connect(self.broker, self.port)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        td.Thread(target=self.client.loop_forever).start()
        

    # Métodos de comunicação mqtt para lidar com conexão, mensagem
    def on_connect(self, client, userdata, flags, rc):
        print("Conexão estabelecida com o código de retorno: {}".format(rc))
        # Inscreve-se em um tópico
        client.subscribe("/vagas3")
      
        
    
    def on_message(self, client, userdata, message):
        print("Mensagem recebida no tópico: {}, msg: {}  nível QoS {}".format(message.topic,
                                                                            message.payload.decode(),
                                                                            message.qos))
        if(message.topic == "/vagas3"):
            print("vou mandar as minha vagas")
            msg = json.dumps({"name": self.name, "vacancy": self.queue}).encode()
            if(self.queue > 0):
                self.queue -= 1
            time.sleep(0.1)
            self.client.publish("/num_vagas3", msg)
            if(self.queue > 0):
                self.queue -= 1


# inicialização do posto
if __name__ == '__main__':
    # inicialização do posto
    client = EletricStation(name="P3", address='localhost', port=1883, vacancy=0)
    