import Car
import Broker
from Eletric_station import EletricStation
import threading


if __name__ == "__main__":

    bk = Broker.BrokerSRV('localhost','bk1' ,1883)

    # eletric_station = EletricStation()
    cl = Car.Client("car1", 'localhost', 1883,100)
    
    cl_thread = threading.Thread(target=cl.send_msg)
    cl_thread.start()