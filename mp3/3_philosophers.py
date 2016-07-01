from threading import Thread, Semaphore
from time import sleep
from timeit import Timer
import random
import sys


philospers=0
meals_target=0
if __name__ == '__main__':
    if len(sys.argv) == 3:
        philospers = int(sys.argv[1])
        meals_target = int(sys.argv[2])
    else:
        print("Wrong arguments!! EXIT!!")
        exit()
    forks = [Semaphore(1) for i in range(philospers)]
    footman = Semaphore(philospers - 1)

rng = random.Random()
rng.seed(100)


def left(i):
    if i < 0:
        return i + philospers
    return i


def right(i): return (i + 1) % philospers


def footman_get_forks(i):
    footman.acquire()
    forks[right(i)].acquire()
    forks[left(i)].acquire()


def footman_put_forks(i):
    forks[right(i)].release()
    forks[left(i)].release()
    footman.release()


def footman_solution(i):
    # print("Start: ",i,"\n")
    for meals in range(meals_target):
        footman_get_forks(i)
        # print("meals: ",meals,"\n")
        sleep(rng.random() / 100)
        footman_put_forks(i)
        sleep(rng.random() / 100)


def footman_run():
    global philospers

    ts = [Thread(target=footman_solution, args=[i]) for i in range(philospers)]
    for t in ts: t.start()
    for t in ts: t.join()


def leftie_get_forks(i):
    forks[left(i)].acquire()
    forks[right(i)].acquire()


def rightie_get_forks(i):
    forks[right(i)].acquire()
    forks[left(i)].acquire()


def leftie_put_forks(i):
    forks[left(i)].release()
    forks[right(i)].release()


def rightie_put_forks(i):
    forks[right(i)].release()
    forks[left(i)].release()


def leftie_solution(i):
    for meals in range(meals_target):
        leftie_get_forks(i)
        # print("meals: ", meals, "\n")
        sleep(rng.random() / 100)
        leftie_put_forks(i)
        sleep(rng.random() / 100)


def rightie_solution(i):
    for meals in range(meals_target):
        rightie_get_forks(i)
        # print("meals: ", meals, "\n")
        sleep(rng.random() / 100)
        rightie_put_forks(i)
        sleep(rng.random() / 100)


def xxxties_run():
    global philospers
    # Random choose number of lefties and righties
    lefties = rng.randint(1, philospers - 1)
    lts = [Thread(target=leftie_solution, args=[i]) for i in range(lefties)]
    rts = [Thread(target=rightie_solution, args=[i]) for i in range(lefties, philospers)]
    for t in lts: t.start()
    for t in rts: t.start()
    for t in lts: t.join()
    for t in rts: t.join()


state = ['thinking'] * philospers
sem = [Semaphore(0) for i in range(philospers)]
mutex = Semaphore(1)
hungryLevel = [0] * philospers


def t_get_fork(i):
    mutex.acquire()
    state[i] = 'hungry'
    t_test(i)
    mutex.release()
    sem[i].acquire()


def t_put_fork(i):
    mutex.acquire()
    state[i] = 'thinking'
    minMeal = meals_target
    minIndex = 0
    for j in range(philospers):
        if hungryLevel[j] < minMeal:
            minIndex=j
            minMeal=hungryLevel[j]
    t_test(minIndex)
    t_test(right(i))
    t_test(left(i - 1))
    mutex.release()


def t_test(i):
    if state[i] == 'hungry' and \
                    state[left(i - 1)] != 'eating' and \
                    state[right(i)] != 'eating':
        state[i] = 'eating'
        sem[i].release()


def t_solution(i):
    # print("Start: ",i,"\n")
    for meals in range(meals_target):
        t_get_fork(i)
        # print("meals: ", meals, "\n")
        hungryLevel[i] += 1
        sleep(rng.random() / 100)
        t_put_fork(i)
        sleep(rng.random() / 100)


def t_run():
    global philospers

    ts = [Thread(target=t_solution, args=[i]) for i in range(philospers)]
    for t in ts: t.start()
    for t in ts: t.join()


if __name__ == '__main__':

    # Re-seed rng every tests
    rng.seed(100)
    timer1 = Timer(footman_run)
    print("1. Footman solution, time elapsed:\t{:0.3f}s".format(timer1.timeit(10) / 10))

    rng.seed(100)
    #forks = [Semaphore(1) for i in range(philospers)]
    timer2 = Timer(xxxties_run)
    print("2. Left-handed solution, time elapsed:\t{:0.3f}s".format(timer2.timeit(10) / 10))

    rng.seed(100)
    timer3 = Timer(t_run)
    print("3. Tanenbaum's solution, time elapsed:\t{:0.3f}s".format(timer3.timeit(10) / 10))
