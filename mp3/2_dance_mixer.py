import itertools
from collections import deque
from threading import Thread, Semaphore
from time import sleep
import random


class LightSwitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Semaphore(1)

    def lock(self, semaphore):
        self.mutex.acquire()
        self.counter += 1
        if self.counter == 1:
            semaphore.acquire()
        self.mutex.release()

    def unlock(self, semaphore):
        self.mutex.acquire()
        self.counter -= 1
        if self.counter == 0:
            semaphore.release()
        self.mutex.release()


rng = random.Random()
leaders = 10
followers = 50


danceLeader = -1
danceFollower = -1

# add leaders and followers into queues
leaderQueue = deque([])
for i in range(leaders):
    leaderQueue.append(i)

followerQueue = deque([])
for i in range(followers):
    followerQueue.append(i)


# Rendevous
leaderArraival = Semaphore(0)
followerArraival = Semaphore(0)

play = Semaphore(0)

leadermutex = Semaphore(1)
followermutex = Semaphore(1)

leaderqueuemutex = Semaphore(1)
followerqueuemutex = Semaphore(1)

leaderdance = Semaphore(0)
followerdance = Semaphore(0)

dancestart = Semaphore(0)


####band part####
turnstile = Semaphore(0)
leaderEmpty = Semaphore(0)
followerEmpty = Semaphore(0)
lsLeader = LightSwitch()
lsFollower = LightSwitch()


def start_music(music):
    turnstile.release()
    leaderEmpty.release()
    followerEmpty.release()
    print("** Band leader started playing ", music, " **")


def end_music(music):
    # print("** Band leader stopping playing ", music, " **")
    turnstile.acquire()
    followerEmpty.acquire()
    leaderEmpty.acquire()
    print("** Band leader stopped playing ", music, " **")


def enter_floor(str, i):
    print(str, i, " entering floor.")


def dance(queue):
    global danceLeader, danceFollower
    followerdance.acquire()
    leaderdance.acquire()
    if (danceFollower != -1) and (danceLeader != -1):
        print("Leader ", danceLeader, " and Follower ", danceFollower, " are dancing.")
        danceLeader = -1
        danceFollower = -1
        dancestart.release()


def line_up(queue, i):
    if queue == leaderQueue:
        leaderqueuemutex.acquire()
        queue.append(i)
        leaderqueuemutex.release()
        print("Leader ", i, " getting back in line.")

    if queue == followerQueue:
        followerqueuemutex.acquire()
        queue.append(i)
        followerqueuemutex.release()
        print("Follower ", i, " getting back in line.")


def band_leader():
    for music in itertools.cycle(['waltz', 'tango', 'foxtrot']):
        start_music(music)
        sleep(5)
        end_music(music)


def dance_leader():
    global danceLeader
    while True:
        turnstile.acquire()
        turnstile.release()
        leadermutex.acquire()
        leaderArraival.release()
        followerArraival.acquire()
        lsLeader.lock(leaderEmpty)
        leaderqueuemutex.acquire()
        # Check the length of the queue
        # if no dancer than go back
        if len(leaderQueue) == 0:
            leaderqueuemutex.release()
            lsLeader.unlock(leaderEmpty)
            leadermutex.release()
            sleep(0)
            continue
        else:
            i = leaderQueue.popleft()
            leaderqueuemutex.release()

        enter_floor("Leader ", i)
        danceLeader = i
        leaderdance.release()
        dance(leaderQueue)
        leadermutex.release()
        sleep(rng.random())
        line_up(leaderQueue, i)
        lsLeader.unlock(leaderEmpty)


def dance_follower():
    global danceFollower
    while True:
        turnstile.acquire()
        turnstile.release()
        followermutex.acquire()
        followerArraival.release()
        leaderArraival.acquire()
        lsFollower.lock(followerEmpty)
        followerqueuemutex.acquire()
        # same story like dance_leader
        if len(followerQueue) == 0:
            followerqueuemutex.release()
            lsFollower.unlock(followerEmpty)
            followermutex.release()
            sleep(0)
            continue
        else:
            i = followerQueue.popleft()
            followerqueuemutex.release()

        enter_floor("Follower ", i)

        danceFollower = i
        followerdance.release()
        dancestart.acquire()
        followermutex.release()
        sleep(rng.random())
        line_up(followerQueue, i)
        lsFollower.unlock(followerEmpty)


if __name__ == '__main__':
    ts = [Thread(target=dance_leader) for i in range(leaders)]
    i = 0
    for t in ts:
        t.start()
    ts = [Thread(target=dance_follower) for i in range(followers)]
    for t in ts: t.start()

    Thread(target=band_leader).start()
