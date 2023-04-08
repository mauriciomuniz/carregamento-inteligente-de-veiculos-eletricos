import paho.mqtt.client as mqtt
import threading as td
import json
import variables as vb
import warshall as ws
#import Eletric_station as es

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
        self.orig = ''
        self.list_dis_que = []

        #self.init_station()
        td.Thread(target=self.client.loop_forever).start()
        self.wars = ws.Warshall()
        

    '''def init_station(self):
        for p in vb.VERTICES:
            if("P" in p):
                self.stations.append(es.EletricStation(p))'''
                

    # Define a função de callback que será chamada quando uma mensagem for recebida
    def on_message(self, client, userdata, message):
        print("Mensagem recebida no tópico: {}, msg: {}  nível QoS {}".format(message.topic,
                                                                            message.payload.decode(),
                                                                            message.qos))
        self.select_topic(message)
        

    def select_topic(self, msg):
        if(msg.topic == "/location"):
            self.location(msg)
            self.client.publish("/vagas", "há quantas vagas")
        if(msg.topic == "/num_vagas"):
            self.response(msg)
        
    # Define a função de callback que será chamada
    # quando a conexão for estabelecida
    def on_connect(self, client, userdata, flags, rc):
        print("Conexão estabelecida com o código de retorno: {}".format(rc))

        # Inscreve-se em um tópico
        self.client.subscribe("/num_vagas") 
        self.client.subscribe("/location") # Recebe a localização do carro
       

    # Define a função de callback que será chamada quando a conexão for perdida
    def on_disconnect(self, client, userdata, rc):
        print("Conexão perdida com o código de retorno: {}".format(rc))

    '''
        Função que recebe a localização do carro
    '''
    def location(self,msg):
        dict_msg = json.loads(msg.payload.decode())
        self.orig = dict_msg.get('localizacao')


    '''
        Falta fazer a parte de verificar se todos os postos tem vagas, ou seja, diferente de 0.
    '''

    def response(self, msg):
        dict_msg = json.loads(msg.payload.decode())
        local = dict_msg["name"] 
        dict_msg["dis_que"] = (self.wars.dis[self.orig][vb.VERTICES.index(local)], dict_msg.get("vacancy")) # Cria uma tupla com a distância e o número de vagas do posto
        self.list_dis_que.append(dict_msg)
        del dict_msg["vacancy"]

        if(len(self.list_dis_que) == self.num_station()):
            self.list_dis_que.sort(key=lambda short: short["dis_que"]) 
            list_path = self.wars.constructPath(self.orig, vb.VERTICES.index(self.list_dis_que[0].get("name")))

            print("Vá para o posto {} seguindo a rota: {}\nDistância de {}km".format(
                self.list_dis_que[0].get("name"), self.wars.printPath(list_path),vb.VERTICES.index(local)))  
        
    def num_station(self):
        i = 0
        for p in vb.VERTICES:
            if("P" in p):
                i+=1
        return i
