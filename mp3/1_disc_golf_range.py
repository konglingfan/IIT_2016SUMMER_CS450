from threading import Thread, Semaphore
from time import sleep
import random
rng = random.Random()

# Parameters can be modified
stash = 20
N = 5 # Number of discs per bucket
frolfers = 4 # Number of frolfers

# Variables
discs_on_field = 0


emptyStash = Semaphore(0)
fullStash = Semaphore(0)
mutex = Semaphore(1)
turnstile = Semaphore(1)


def frolfer(num):
    global stash
    global discs_on_field
    rng.seed(100)
    while True:
        turnstile.acquire()
        turnstile.release()
        mutex.acquire()
        print("Frolfer ", num, " calling for bucket")
        if stash < N:
            emptyStash.release()
            fullStash.acquire()
            discs_on_field = 0
        stash -= N  # call for bucket
        mutex.release()
        print("Frolfer ", num, " got ", N, " discs; Stash = ", stash)
        for i in range(0, N):  # for each disc in bucket,
            mutex.acquire()
            discs_on_field += 1  # throw (maybe simulate with a random sleep)
            print("Frolfer ", num, " threw disc ", i)
            mutex.release()
            sleep(rng.random())


def cart():
    global stash
    global discs_on_field
    while True:
        emptyStash.acquire()
        turnstile.acquire()
        print("################################################################################")
        print("Stash = ", stash, "; Cart entering field")
        stash += discs_on_field  # collect discs and deposit in stash
        print("Cart done, gathered ", discs_on_field, " discs; Stash = ", stash)
        print("################################################################################")
        turnstile.release()
        fullStash.release()


if __name__ == '__main__':
    ts = [Thread(target=frolfer, args=[i]) for i in range(frolfers)]
    for t in ts: t.start()
    Thread(target=cart).start()
