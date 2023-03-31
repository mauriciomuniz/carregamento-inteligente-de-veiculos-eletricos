import Car
import Broker

if __name__ == "__main__":

    bk = Broker.BrokerSRV('localhost','bk1' ,1883)

    cl = Car.Client("car1", 'localhost', 1883).send_msg()