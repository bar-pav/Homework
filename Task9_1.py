
# Deadlock

from threading import Thread, Lock

forks = [Lock() for f in range(5)]


def get_fork(phil_num, fork):
    fork_n = (phil_num + fork) % 5
    forks[fork_n].acquire()
    print("Philosopher " + str(phil_num) + " get fork " + str(fork_n))


def put_fork(phil_num, fork):
    fork_n = (phil_num + fork) % 5
    forks[fork_n].release()
    print("Philosopher " + str(phil_num) + " put fork " + str(fork_n))


def eat(phil_num):
    while True:
        get_fork(phil_num, 0)
        get_fork(phil_num, 1)
        print("Philosopher " + str(phil_num) + " eats...")
        print("Philosopher " + str(phil_num) + " finished eating")
        put_fork(phil_num, 0)
        put_fork(phil_num, 1)


p1 = Thread(target=eat, args=(1,))
p2 = Thread(target=eat, args=(2,))
p3 = Thread(target=eat, args=(3,))
p4 = Thread(target=eat, args=(4,))
p5 = Thread(target=eat, args=(5,))



def think():
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()


think()
