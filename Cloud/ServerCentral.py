import socket 
import threading
from time import sleep
import file
import linked_list
import json
import ClientTCP

class Server:
    
    def __init__(self, host='localhost', port_TCP=5555):
        self.host = host
        self.port_TCP = port_TCP
        self.data_payload = 2048 
        self.list_servers = file.read("./servers.json")
        # Cria uma lista duplamente encadeada para navegar entres os servidores
        self.linked_list = linked_list.LinkedListDuple()
        
        # Preenche a lista com os servidores existente no arquivo
        self.insert_in_linked_list()
        
        self.save_server = None
        
        
    '''
        Realiza uma busca do servidor atual que solicitou ao server central e busca o próximo servidor. 
        Caso não exista o próximo, busca o anterior. 
    '''    
    def search_server(self, srv):
        
        # Encontra o servidor e salva em uma variável 
        if(self.linked_list.size > 1):
            self.server = self.linked_list.find_node(srv) 
            if(self.server):
                self.server.visited = True
        
                # Se for o início da lista, será buscado o próximo da lista
                if(self.linked_list.is_head(self.server) or self.server.next):
                    return self.server.next
                #Se for o final da lista, será buscado o anterior.
                elif(self.linked_list.is_tail(self.server) or self.server.previous):
                    return self.server.previous
          
        return None
    
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
    Recebe clientes e suas respectivas mensagens http
    '''
    def handle_client_TCP(self, client, addr):
        print("New connection by {}".format(addr))
        data = client.recv(1024)
        if data:  
            data_server = json.loads(data.decode())
            other_server = self.search_server(data_server.get('name_server'))# obtém o nome do servidor que fez a conexão
            resp = json.dumps({"position":data_server.get("position_car")})
            
            print(f'Se conecte ao server: {other_server.data}')
            
            if(other_server):            
                # Servidor central obtém o dados do próximo servidor(broker) para se comunicar
                s = ClientTCP.Client_TCP(other_server.data.get("ip"), other_server.data.get("port")) 
                # Resposta do broker
                resp_broker = s.connect(resp) #Envia um mensagem para o servidor que deseja obter a resposta
                print(f'resposta do server- {other_server.data.get("name")} reps- {resp_broker}')
                
                self.search_server(other_server.data.get("name"))
                
                # Responde o server 
                client.send(resp_broker.encode())
            else:
                 client.send("Não há mais servidor para pesquisar")
    
    
              
        client.close()  
        print("Close connection")
        
        
s = Server()
s.connect()