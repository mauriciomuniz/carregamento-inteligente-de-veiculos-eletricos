import sys
sys.path.insert(1, '../')

import paho.mqtt.client as mqtt
import threading as td
import json
import variables as vb
import Controller.warshall as ws
import time

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
    
                

    # Define a função de callback que será chamada quando uma mensagem for recebida
    def on_message(self, client, userdata, message):
        print("Mensagem recebida no tópico: {}, msg: {}  nível QoS {}".format(message.topic,
                                                                            message.payload.decode(),
                                                                            message.qos))
        self.select_topic(message)
        

    def select_topic(self, msg):
        if(msg.topic == "/location2"):
            self.location(msg)
            self.client.publish("/vagas2", "há quantas vagas")
        if(msg.topic == "/num_vagas2"):
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
        self.client.subscribe("/num_vagas2") 
        self.client.subscribe("/location2") # Recebe a localização do carro
        self.client.subscribe(self.id)
        self.client.subscribe("/pegar_vagas2") 
        self.client.subscribe('/receber2_posto')


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
        
    # cria um obj json e adiciana em uma lista de postos 
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
            msg =  json.dumps({"position_car": self.orig, "id":self.id}).encode()
            self.client.publish("/procurar_postos2", msg)
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
       
        '''all_vacancies = all([p["vacancy"] != 0 for p in self.stations])
        
        if all_vacancies:
            dict_msg["dis_que"] = (self.wars.dis[self.orig][vb.VERTICES.index(local)], vacancy -1) # Cria uma tupla com a distância e o número de vagas do posto
            self.list_dis_que.append(dict_msg)
            del dict_msg["vacancy"]

            if(len(self.list_dis_que) == self.num_station()):   
                self.list_dis_que.sort(key=lambda short: short["dis_que"]) 
                list_path = self.wars.constructPath(self.orig, vb.VERTICES.index(self.list_dis_que[0].get("name")))

                # Diminui em -1 o número de vagas do posto escolhido
                for p in self.stations:
                    if p["name"] == self.list_dis_que[0].get("name"):
                        p["vacancy"] -= 1
                        break    
                
                print("Vá para o posto {} seguindo a rota: {}\nDistância de {}km".format(
                    self.list_dis_que[0].get("name"), self.wars.printPath(list_path),vb.VERTICES.index(local)))  
        '''




    def num_station(self):
        i = 0
        for p in vb.VERTICES:
            if("P" in p):
                i+=1
        return i


bk = BrokerSRV('localhost','bk2' ,1883)