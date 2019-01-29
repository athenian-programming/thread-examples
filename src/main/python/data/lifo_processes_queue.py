#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from queue import Empty
from random import randrange


def producer(queue, lock, completed_event):
    for i in range(20):
        data = "image-{0}".format(i)
        with lock:
            # The queue will be full if the last item assigned has not already been read
            if queue.full():
                discarded = queue.get()
                print("Discarded: {}".format(discarded))
            queue.put(data)
        # Pause a random amount of time
        time.sleep(randrange(3))
    completed_event.set()
    print("Producer finished")


def consumer(queue, lock, completed_event):
    while not completed_event.is_set() or queue.qsize() > 0:
        with lock:
            try:
                data = queue.get_nowait()
                if data is not None:
                    print("Consumed: {}".format(data))
            except Empty:
                # Keep going if no value is ready to be read
                pass
        # Pause a random amount of time
        time.sleep(randrange(3))
    print("Consumer finished")


def main():
    # Create Manager to grab a queue and an event
    manager = Manager()
    # Set the maximum size of the Queue to be 1
    queue = manager.Queue(maxsize=1)
    lock = manager.Lock()
    completed_event = manager.Event()

    with ProcessPoolExecutor() as executor:
        executor.submit(consumer, queue, lock, completed_event, )
        executor.submit(producer, queue, lock, completed_event, )


if __name__ == "__main__":
    main()
