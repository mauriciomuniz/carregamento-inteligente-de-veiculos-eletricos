import sys
sys.path.insert(1, '../')

import paho.mqtt.client as mqtt
import threading as td
import json
import variables as vb
import Controller.warshall as ws
import time
import ServerTCP
import json

# Classe que representa o primeiro broker
class BrokerSRV():

    def __init__(self,address, name, port) -> None:
        self.client_name = name 
        self.broker_port = port
        self.broker_address = address
        # Cria uma instância do cliente MQTT
        self.client = mqtt.Client(self.client_name)

        # Define as funções de callback do cliente eturnMQTT
        self.client.on_message =self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
        # Conecta-se ao broker MQTT
        self.client.connect(self.broker_address, self.broker_port)
        self.id = f'id_{self.client_name}'
        self.stations = []
        self.orig = ''
        self.list_dis_que = []
        self.who_req = False
        self.id_client = ''
        self.id_car = None
        
        td.Thread(target=self.client.loop_forever).start()
        
        self.wars = ws.Warshall()
        
        # servidor tpc criado para interação com outros servidores
        self.server = ServerTCP.ServerFOG("server2",'localhost', 60000)
        self.server.connect()
        td.Thread(target=self.client_connect_TCP).start()
      
                   


    def client_connect_TCP(self):
        while True:
            print ("Waiting to receive message from client")
            client, address = self.server.con_socket.accept() 
            td.Thread(target=self.handle_client_TCP, args=(client, address), daemon=True).start()
     
    '''
    Recebe do servidor central requisições
    '''
    def handle_client_TCP(self, client, addr): 
        print("New connection by {}".format(addr))
        data = client.recv(1024)
        if data:
            self.who_req = True
            self.message = data.decode()
            self.orig = json.loads(self.message).get("position")
            # Publica para os postos enviarem os estados das filas
            self.client.publish("/vagas2")
            time.sleep(2)
            resp = self.response("")
            print(resp)
            client.send(resp.encode())
            
        client.close()  
        print("Close connection")


    # Define a função de callback que será chamada quando uma mensagem for recebida
    def on_message(self, client, userdata, message):
        print("Mensagem recebida no tópico: {}, msg: {}  nível QoS {}".format(message.topic,
                                                                            message.payload.decode(),
                                                                            message.qos))
        self.select_topic(message)
        
    # tópicos a serem selecionados, a depender do tópico faz uma ação
    # Se o tópico for /location, então ele vai buscar a localização baseada no carro atual e publica no 
    # topico de /vagas e msg de quantas vagas tem
    # Se o tópico for /num_vagas, então ele busca o numero de vagas nos postos
    def select_topic(self, msg):
        if(msg.topic == "/location2"):
            self.location(msg)
            self.client.publish("/vagas2", "há quantas vagas")
        if(msg.topic == "/num_vagas2"):
            print(self.who_req)
            if(self.who_req):
                self.receive_stations(msg)
            else:
                self.receive_stations(msg)
                time.sleep(0.1)
                self.response(msg)
                
        
    def dict_msg(self, msg):
        return json.loads(msg.payload.decode())
        
    # Define a função de callback que será chamada
    # quando a conexão for estabelecida
    def on_connect(self, client, userdata, flags, rc):
        print("Conexão estabelecida com o código de retorno: {}".format(rc))

        # Inscreve-se em um tópico
        self.client.subscribe("/num_vagas2") 
        self.client.subscribe("/location2",qos=1) # Recebe a localização do carro
        self.client.subscribe(self.id)
        

    # Define a função de callback que será chamada quando a conexão for perdida
    def on_disconnect(self, client, userdata, rc):
        print("Conexão perdida com o código de retorno: {}".format(rc))

    '''
        Função que recebe a localização do carro
    '''
    def location(self,msg):
        dict_msg = self.dict_msg(msg)
        self.orig = dict_msg.get('localizacao')
        self.id_car = dict_msg.get('id_car')
       
       
    # recebe as estações com nome, quantidade de vagas, distancia e fila
    # tbm cria um obj json e adiciona em uma lista de postos por causa do da função dict_msg
    def receive_stations(self, msg):
        print("Recebendo dados dos postos")
        dict_msg = self.dict_msg(msg)
        local = dict_msg["name"] 
        vacancy = dict_msg.get("vacancy")
        if(vacancy > 0):
            self.stations.append({"station":local, 
                                    "dist_and_queue":((self.wars.dis[self.orig][vb.VERTICES.index(local)], vacancy))})
     
    
    def response(self, msg):
        # Se a lista de estação for 0 e não foi o servidor que solicitou a conexão
        # ou seja, foi o carro. Então uma conexão com o servidor central é estbelecida
        if(len(self.stations) == 0 and not self.who_req):
            msg =  json.dumps({"name_server":self.server.name,"position_car": self.orig})
            # Envia uma mensagem informando o nome do server e a posicao do carro
            self.resp_from_server_central = self.server.send_to_srv_central(msg)
            
            print(f'Responda para o server {self.resp_from_server_central}')
            if(self.resp_from_server_central == "0"):
                self.client.publish(f'/{self.id_car}', "Não foi possível encontrar um posto. aguarde...")
            else:
                resp = json.loads(self.resp_from_server_central)
                self.client.publish(f'/{self.id_car}', self.format_string(resp.get("path"),resp.get("station"),resp.get("dist")))

        elif(self.who_req):
            if(len(self.stations) > 0):
                self.stations.sort(key=lambda short: short["dist_and_queue"]) 
                station_name = self.stations[0].get("station")
            
                # Lista de caminhos onde recebe a origem e os vertices com o índice de nome das estações
                list_path = self.wars.constructPath(self.orig, vb.VERTICES.index(station_name))
                dist = self.wars.dis[self.orig][vb.VERTICES.index(station_name)]
            
                print("Encontrei postos com vagas solicitada pelo servidor central")
                self.clear_variables()
                return json.dumps({"path":list_path, "station": station_name, "dist": dist})
            
            else:
                self.clear_variables()
                return "0" # Retorna para o servidor central informando 0 que significa que não tinham postos com vagas
             
        if(len(self.stations) > 0):
            #Realiza a publicação para o carro que solicitou
            self.stations.sort(key=lambda short: short["dist_and_queue"]) 
            station_name = self.stations[0].get("station")
            
            # Lista de caminhos onde recebe a origem e os vertices com o índice de nome das estações
            list_path = self.wars.constructPath(self.orig, vb.VERTICES.index(station_name))
            dist = self.wars.dis[self.orig][vb.VERTICES.index(station_name)]
            
            self.client.publish(f'/{self.id_car}', self.format_string(list_path, station_name, dist))

        self.clear_variables()
        
    
    '''
    Limpa as variáveis para manter o contexto padrão depois da execução
    '''
    def clear_variables(self):
        self.orig = None
        self.stations.clear()
        self.who_req = False
        self.id = None
        
        
    def format_string(self, path, station, dist):
        return "Vá para o posto {} seguindo a rota: {}\nDistância de {}km".format(
                     station, self.wars.printPath(path), dist)
       
        
       
   

bk = BrokerSRV('localhost','bk2' ,1883)