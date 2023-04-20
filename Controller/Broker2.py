import sys
sys.path.insert(1, '../')

import paho.mqtt.client as mqtt
import threading as td
import json
import variables as vb
import Controller.warshall as ws
import time
import ServerTCP

# Classe que representa o segundo broker
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
        self.id = f'id_{self.client_name}'
        self.stations = []
        self.orig = ''
        self.list_dis_que = []
        self.who_req = ''
        self.id_client = ''
        #self.init_station()
        td.Thread(target=self.client.loop_forever).start()
        self.wars = ws.Warshall()
        self.server = ServerTCP.ServerFOG("server2",'localhost', 60000)
        self.server.connect()
        
        
       
                

    # Define a função de callback que será chamada quando uma mensagem for recebida
    def on_message(self, client, userdata, message):
        print("Mensagem recebida no tópico: {}, msg: {}  nível QoS {}".format(message.topic,
                                                                            message.payload.decode(),
                                                                            message.qos))
        self.select_topic(message)
        
    # tópicos a serem selecionados, a depender do tópico faz uma ação
    # Se o tópico for /location, então ele vai buscar a localização baseada no carro atual e publica no 
    # topico de /vagas e msg de quantas vagas tem
    # Se o tópico for /num_vagas, então ele busca o numero de vagas naquele posto
    # se for /receber_posto, então teremos o posto e a distância até ele
    def select_topic(self, msg):
        if(msg.topic == "/location"):
            self.location(msg)
            self.client.publish("/vagas", "há quantas vagas")
        if(msg.topic == "/num_vagas"):
            self.receive_stations(msg)
            time.sleep(0.5)
            self.response(msg)
        if(msg.topic == "/receber_posto"):
            mes_rec = self.dict_msg(msg)
            self.format_string(mes_rec.get("path"), mes_rec.get("station"), mes_rec.get("dist"))
    
    def dict_msg(self, msg):
        return json.loads(msg.payload.decode())
        
    # Define a função de callback que será chamada
    # quando a conexão for estabelecida
    def on_connect(self, client, userdata, flags, rc):
        print("Conexão estabelecida com o código de retorno: {}".format(rc))

        # Inscreve-se em um tópico
        self.client.subscribe("/num_vagas") 
        self.client.subscribe("/location") # Recebe a localização do carro
        self.client.subscribe(self.id)
        self.client.subscribe("/pegar_vagas") 
        self.client.subscribe('/receber_posto')

    # Define a função de callback que será chamada quando a conexão for perdida
    def on_disconnect(self, client, userdata, rc):
        print("Conexão perdida com o código de retorno: {}".format(rc))

    '''
        Função que recebe a localização do carro
    '''
    def location(self,msg):
        dict_msg = self.dict_msg(msg)
        self.orig = dict_msg.get('localizacao')
        self.who_req = dict_msg['request']
        self.id_client = dict_msg.get('id_car')
        
    # recebe as estações com nome, quantidade de vagas, distancia e fila
    # tbm cria um obj json e adiciona em uma lista de postos por causa do da função dict_msg
    def receive_stations(self, msg):
        dict_msg = self.dict_msg(msg)
        local = dict_msg["name"] 
        vacancy = dict_msg.get("vacancy")
        if(vacancy > 0):
            self.stations.append({"station":local, 
                                    "dist_and_queue":((self.wars.dis[self.orig][vb.VERTICES.index(local)], vacancy)), 
                                    #"path_total":self.wars.constructPath(self.orig, vb.VERTICES.index(p)),
                                    })
     
    
    def response(self, msg):
    
        if(len(self.stations) == 0 ):
            msg =  json.dumps({"name_server":self.server.name,"position_car": self.orig})
            send_server_central = self.server.send_to_srv_central(msg)
            #response = requestServer.connect(msg)
            #self.client.publish("/procurar_postos", msg)
        else:
            self.stations.sort(key=lambda short: short["dist_and_queue"]) 
            station_name = self.stations[0].get("station")
            
            list_path = self.wars.constructPath(self.orig, vb.VERTICES.index(station_name))
            dist = self.wars.dis[self.orig][vb.VERTICES.index(station_name)]
            if(self.who_req == "server"):
                print("Encontrei postos com vagas solicitada pelo servidor")
                msg_return = json.dumps({"path":list_path, "station": station_name, "dist": dist}).encode()
                self.client.publish("/receber_posto", msg_return)
            else:
                self.format_string(list_path, station_name,  dist)
        
        self.orig = ''
        self.stations.clear()
        self.who_req = ''
        self.id = ''
    
    def format_string(self, path, station, dist):
        print("Vá para o posto {} seguindo a rota: {}\nDistância de {}km".format(
                     station, self.wars.printPath(path), dist)) 
       
        
       
   


bk = BrokerSRV('localhost','bk2' ,1883)