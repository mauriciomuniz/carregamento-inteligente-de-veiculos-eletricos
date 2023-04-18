import socket 
import threading
from time import sleep
import ClientTCP

class ServerFOG:
    
    def __init__(self,name ,host,port_TCP):
        self.name = name
        self.host = host
        self.port_TCP = port_TCP
        self.data_payload = 2048 
        self.port_srv_central = 5555
        

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
    Função que aguarda a conexão de clientes.
    '''
    def client_connect_TCP(self):
            while True:
                print ("Waiting to receive message from client")
                client, address = self.con_socket.accept()
                client_thread = threading.Thread(target=self.handle_client_TCP, args=(client, address), daemon=True)
                client_thread.start()
                
    def send_msg(self,client,msg):
            client.send(msg.encode('utf-8')) 
        
                        
    '''
    Recebe clientes e suas respectivas mensagens http
    '''
    def handle_client_TCP(self, client, addr):
        print("New connection by {}".format(addr))
        data = client.recv(1024)
        if data:
            print(data.decode())
        client.close()  
        print("Close connection")
    
   
    def send_to_srv_central(self, msg):
        client = ClientTCP.Client_TCP('localhost', self.port_srv_central)
        client.connect(msg)
        
'''s = ServerFOG("Fog1")
s.connect()
s.send_to_srv_central("Enviando do server 1")'''
    
    
    