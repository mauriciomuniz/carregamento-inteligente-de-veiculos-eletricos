import Car
import threading


car1 = Car.Client("car1", 'localhost', 1883)
threading.Thread(target=car1.send_msg).start()