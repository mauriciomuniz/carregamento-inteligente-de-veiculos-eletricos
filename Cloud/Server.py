import paho.mqtt.client as mqtt_client
import threading
import json

'''
servidor mqtt que é iniciado com um nome, endereço de broker e porta
é definido dois tópicos para procurar postos e para receber postos
'''
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
    '''
    a conexão é estabelecida, a função on_connect é chamada, 
    e o servidor se inscreve em cada um dos tópicos definidos anteriormente.
    '''
    def on_connect(self, client, userdata, flags, rc):
        print("Conexão estabelecida com o código de retorno: {}".format(rc))
        # Inscreve-se em um tópico
        
        for top in self.topic:
            self.client.subscribe(top)

    '''
    a função on_message é chamada, e o servidor trata a mensagem recebida. Se a mensagem recebida estiver
    no tópico /procurar_postos, a função search_station é chamada para procurar a estação de gasolina mais 
    próxima e publicar uma mensagem de resposta. Se a mensagem recebida estiver no tópico /receber_posto, 
    o servidor publica a mensagem recebida no tópico /posto_enc 
    '''   
    
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