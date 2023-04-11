import paho.mqtt.client as mqtt_client
import threading
import json

class Server():
    def __init__(self, name, address, port) -> None:
        self.name = name
        

        self.broker = address
        self.port = port
        self.topic = ["/procurar_postos", "/recebe_posto"]
    
        
        self.client = mqtt_client.Client(name)
        self.client.connect(self.broker, self.port)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        threading.Thread(target=self.client.loop_forever).start()


    def on_connect(self, client, userdata, flags, rc):
        print("Conexão estabelecida com o código de retorno: {}".format(rc))
        # Inscreve-se em um tópico
        
        for top in self.topic:
            self.client.subscribe(top)

        
    
    def on_message(self, client, userdata, message):
        print("Mensagem recebida no tópico: {}, msg: {}  nível QoS {}".format(message.topic,
                                                                            message.payload.decode(),
                                                                            message.qos))
        if(message.topic == '/procurar_postos'):
            self.search_station(message)
        if(message.topic == '/receber_posto'):
            self.client.publish('/posto_enc', message)

    def search_station(self, msg):
        dict_bk = json.loads(msg.payload.decode())
        id_broker = dict_bk.get("id") + 1
        print(type(id_broker))
        msg = json.dumps({"localizacao":dict_bk["position_car"], "request":self.name}).encode()

        self.client.publish(f"/location{id_broker}", msg)
       
        
        '''
        1° O broker recebe a posição do carro
        2° O broker irá pedir ao primeiro, segundo ou terceiro mais próximo do carro
        3° O broker irá enviar o posto mais próximo do carro
        '''

Server("server", 'localhost', 1883)