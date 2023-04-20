import socket 
import threading
from time import sleep
import ClientTCP

# Esse serverfog representa uma classe de servidor tcp que pode se conectar a outros clientes tcp
# e enviar mensagens a um servidor central. Recebe seus atributos e a porta do servidor central
# 
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
    Função que aguarda a conexão de clientes. Aqui é criado um socket tcp passando o host e porta e começa
    a ouvir conexões tcp. É criado uma thread para lidar com a conexão. O método handle_client_tcp é
    responsável por receber as msg do client tcp e fechar a conexão. E o send msg envia uma msg para o client tcp
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
    
   # envia uma mensagem para o servidor central usando um client tcp. Aqui é criado uma instância da classe 
   # Client_TCP e é conectado ao servidor central pelo método de conexão 
    def send_to_srv_central(self, msg):
        client = ClientTCP.Client_TCP('localhost', self.port_srv_central)
        client.connect(msg)
        
'''s = ServerFOG("Fog1")
s.connect()
s.send_to_srv_central("Enviando do server 1")'''
    
    
    