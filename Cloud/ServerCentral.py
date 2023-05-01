import socket 
import threading
from time import sleep
import file
import linked_list
import json
import ClientTCP


class Server:
    
    def __init__(self, host, port_TCP):
        self.host = host
        self.port_TCP = port_TCP
        self.data_payload = 2048 
        
        # Carrega os servidores do arquivo para a memória
        self.list_servers = file.read("./servers.json")
        
        # Cria uma lista circular encadeada para navegar entres os servidores
        self.linked_list = linked_list.LinkedListCircular()
        
        # Preenche a lista com os servidores existente no arquivo
        self.insert_in_linked_list()
    
        
    
    '''
    Insere os servidores na lista duplamente encadeada
    '''
    def insert_in_linked_list(self):
        for srv in (self.list_servers):
            self.linked_list.insert_init(srv)
            
    ''' 
    connect(), um socket é criado e a conexão é aguardada. Na função client_connect_TCP(), 
    um thread é iniciado para lidar com a conexão do cliente  
    '''  
    def connect(self):
        try:
            self.con_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.con_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_address = (self.host, self.port_TCP)
            self.con_socket.bind(self.server_address)
            self.con_socket.listen()
            
            print ("Starting up echo server TCP on:{} port:{}".format(self.host,self.port_TCP, self.host))
            threading.Thread(target=self.client_connect_TCP).start()
          
        except:
            print("Fail when starting the server")

            
    '''
    Função que aguarda a conexão de clie
            #client.send(response.encode('utf-8')) ntes.
    '''
    def client_connect_TCP(self):
            while True:
                print ("Waiting to receive message from client")
                client, address = self.con_socket.accept()
                client_thread = threading.Thread(target=self.handle_client_TCP, args=(client, address), daemon=True)
                client_thread.start()
                
    '''
    Recebe as requisitções da névoa afim de encontrar uma resposta para indicar o carro ir a um posto
    '''
    def handle_client_TCP(self, client, addr):
        print("New connection by {}".format(addr))
        data = client.recv(1024)
        
        if data:  
            data_server = json.loads(data.decode())
            server_requester = self.linked_list.find_node(data_server.get('name_server'))
            
            next_server = server_requester.next
            resp = json.dumps({"position":data_server.get("position_car")})
            
            # Se existe um proximo servidor
            if(next_server):
                check = "0"
                
                while(check == "0" and server_requester.data.get('name') != next_server.data.get('name')):
                    
                    # Servidor central obtém o dados do próximo servidor/broker para se comunicar
                    print(f'Tentando se conectar ao server {next_server.data.get("name")} porta:{next_server.data.get("port")}')
                    s = ClientTCP.Client_TCP(next_server.data.get("ip"), next_server.data.get("port")) 
                
                    # Resposta do broker
                    check = s.connect(resp) #Envia um mensagem para o servidor que deseja obter a resposta
                    sleep(0.1)
                    next_server = next_server.next
            
                # Responde o server da névoa que solicitou
                client.send(check.encode())
           
            else:
                 client.send("Não há mais servidor para pesquisar")
    
        client.close()  
        print("Close connection")
        
        
s = Server('localhost',5555)
s.connect()