import paho.mqtt.client as mqtt
import threading as td
import disjkstra as dj
import json
import variables as vb
import warshall as ws
import Eletric_station as es

class BrokerSRV():
    def __init__(self,address, name, port) -> None:
        self.client_name = name 
        self.broker_port = port
        self.broker_address = address
        # Cria uma instância do cliente MQTT
        self.client = mqtt.Client(self.client_name)

        # Define as funções de callback do cliente MQTT
        self.client.on_message =self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        # Conecta-se ao broker MQTT
        self.client.connect(self.broker_address, self.broker_port)
        self.stations = []

        self.init_station()
        td.Thread(target=self.client.loop_forever).start()
        self.wars = ws.Warshall()

    def init_station(self):
        for p in vb.VERTICES:
            if("P" in p):
                self.stations.append(es.EletricStation(p))
                

    # Define a função de callback que será chamada quando uma mensagem for recebida
    def on_message(self, client, userdata, message):
        print("Mensagem recebida no tópico: {}, msg: {}  nível QoS {}".format(message.topic,
                                                                            message.payload.decode(),
                                                                            message.qos))
        self.response(message.payload.decode())
        
    # Define a função de callback que será chamada
    # quando a conexão for estabelecida
    def on_connect(self, client, userdata, flags, rc):
        print("Conexão estabelecida com o código de retorno: {}".format(rc))
        # Inscreve-se em um tópico
        client.subscribe("/topico")

    # Define a função de callback que será chamada quando a conexão for perdida
    def on_disconnect(self, client, userdata, rc):
        print("Conexão perdida com o código de retorno: {}".format(rc))


    def response(self,msg):
        dict_msg = json.loads(msg)
        orig = dict_msg.get('localizacao')
       
        d = []
        for p in vb.VERTICES:
            if("P" in p):
                d.append({"station":p, 
                          "dist_and_queue":((self.wars.dis[orig][vb.VERTICES.index(p)], self.find_station(p))), 
                          "path_total":self.wars.constructPath(orig, vb.VERTICES.index(p)),
                        })
        d.sort(key=lambda short: short["dist_and_queue"])

        print("Vá para o posto {} seguindo a rota: {}\nDistância de {}km".format(
            d[0].get("station"), self.wars.printPath(d[0].get("path_total")), d[0].get("dist_and_queue")[0]
        ))   

    # Retorna a quantidade de v
    def find_station(self, name):
        for s in self.stations:
            if(s.name == name):
                return s.queue