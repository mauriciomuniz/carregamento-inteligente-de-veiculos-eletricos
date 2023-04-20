import socket
import json

# aqui temos um client tcp para comunicação entre brokers
# para que possa passar a informação de um broker 
# para o outro
class Client_TCP: 
    def __init__(self, host='localhost', port_TCP=5000):
            self.host = host
            self.port = port_TCP
            self.port_TCP = port_TCP
            self.data_payload = 2048 
            
        
    def connect(self, msg): 
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port_TCP))
            s.send(msg.encode())
            
            # Aguarda a resposta do servidor
            #data = s.recv(1024)
            #print(f"Mensagem do servidor: {data.decode()}")
           
            # Fecha a conexão com o servidor
            s.close()