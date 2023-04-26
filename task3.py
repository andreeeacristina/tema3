"""
Coffee Factory: A multiple producer - multiple consumer approach

Generate a base class Coffee which knows only the coffee name
Create the Espresso, Americano and Cappuccino classes which inherit the base class knowing that
each coffee type has a predetermined size.
Each of these classes have a get message method

Create 3 additional classes as following:
    * Distributor - buffer - A shared space where the producers puts coffees and the consumers takes them
    * CoffeeFactory - producer - An infinite loop, which always sends coffees to the distributor
    * User - consumer -Another infinite loop, which always takes coffees from the distributor

The scope of this exercise is to correctly use threads, classes and synchronization objects.
The size of the coffee (ex. small, medium, large) is chosen randomly everytime.
The coffee type is chosen randomly everytime.

Example of output:

Consumer 65 consumed espresso
Factory 7 produced a nice small espresso
Consumer 87 consumed cappuccino
Factory 9 produced an italian medium cappuccino
Consumer 90 consumed americano
Consumer 84 consumed espresso
Factory 8 produced a strong medium americano
Consumer 135 consumed cappuccino
Consumer 94 consumed americano
"""


import queue
import time
import threading
from threading import Lock, Thread

class Coffee:
    """ Base class """
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_name(self):
        """ Returns the coffee name """
        return self.name

    def get_size(self):
        """ Returns the coffee size """
        return self.size


class Espresso(Coffee):
    """ Espresso implementation """
    def __init__(self, size):
        super().__init__("espresso", size)

    def get_message(self):
        """ Output message """
        return "you got a " + (str)(self.size) + " " + self.name + " coffee"


class Americano(Coffee):
    """ Americano implementation """
    def __init__(self, size):
        super().__init__("americano", size)

    def get_message(self):
        """ Output message """
        return "you got a " + (str)(self.size) + " " + self.name + " coffee"


class Cappuccino(Coffee):
    """ Capuccino implementation """
    def __init__(self, size):
        super().__init__("cappuccino", size)

    def get_message(self):
        """ Output message """
        return "you got a " + (str)(self.size) + " " + self.name + " coffee"


class Distributor:
    def __init__(self, maxsize):
        self.buffer = queue.Queue(maxsize)
        self.maxSize = maxsize

    def get_buffer(self):
        return self.buffer

    def get_maxsize(self):
        return self.maxSize


# producer
class CoffeeFactory(Thread):
    def __init__(self, thread_id, semEmpty, semFull, my_lock, buffer):
        super().__init__()
        self.thread_id = thread_id
        self.semEmpty = semEmpty
        self.semFull = semFull
        self.my_lock = my_lock
        self.buffer = buffer

    def get_id(self):
        return self.thread_id

    def run(self):
        pass

    def run(self):
        while(1):
            time.sleep(1)
            self.semEmpty.acquire()
            self.my_lock.acquire()
            coffee = Americano("large")
            self.buffer.put(coffee)
            print("Producer no " + (str)(self.thread_id) + " produced a " + coffee.get_size() + " " + coffee.get_name())
            self.my_lock.release()
            self.semFull.release()
            time.sleep(1)


# consumer
class User(Thread):
    def __init__(self, thread_id, semEmpty, semFull, my_lock, buffer):
        super().__init__()
        self.thread_id = thread_id
        self.semEmpty = semEmpty
        self.semFull = semFull
        self.my_lock = my_lock
        self.buffer = buffer

    def get_id(self):
        return self.thread_id

    def run(self):
        while(1):
            time.sleep(1)
            self.semFull.acquire()
            self.my_lock.acquire()
            coffee = self.buffer.get()
            print("Consumer no " + (str)(self.thread_id) + ": " + coffee.get_message())
            self.my_lock.release()
            self.semEmpty.release()
            time.sleep(1)


def main():
    consumers = 5
    producers = 5
    distributor_size = 18
    distributor = Distributor(distributor_size)

    semEmpty = threading.Semaphore(distributor.get_maxsize())
    semFull = threading.Semaphore(0)
    my_lock = threading.Semaphore(1)

    consumers_list = []
    producers_list = []

    for i in range(consumers):
        consumer = User(i, semEmpty, semFull, my_lock, distributor.get_buffer())
        consumers_list.append(consumer)
        consumer.start()

    for i in range(producers):
        producer = CoffeeFactory(i, semEmpty, semFull, my_lock, distributor.get_buffer())
        producers_list.append(producer)
        producer.start()

    for i in range(consumers):
        consumers_list[i].join()

    for i in range(producers):
        producers_list[i].join()


if __name__ == '__main__':
    main()
