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


def eat(phil_num, l, r):
    while True:
        get_fork(phil_num, l)
        get_fork(phil_num, r)
        print("Philosopher " + str(phil_num) + " eats...")
        print("Philosopher " + str(phil_num) + " finished eating")
        put_fork(phil_num, l)
        put_fork(phil_num, r)


p1 = Thread(target=eat, args=(1, 1, 0))
p2 = Thread(target=eat, args=(2, 0, 1))
p3 = Thread(target=eat, args=(3, 0, 1))
p4 = Thread(target=eat, args=(4, 0, 1))
p5 = Thread(target=eat, args=(5, 0, 1))



def think():
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()


think()
