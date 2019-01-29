#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from queue import Empty

from random import randrange


def consumer(id, queue, completed_event):
    while not completed_event.is_set():
        print("Waiting on id: {}".format(id))
        try:
            data = queue.get(block=True, timeout=1)
        except Empty:
            continue
        print("Consumed id: {} got data: {}".format(id, data))
    print("Consumer finished")


def producer(queue, completed_event):
    for i in range(10):
        data = "val-{}".format(i)
        print("Producer putting data on queue {}".format(data))
        queue.put(data)
        time.sleep(randrange(2))
    completed_event.set()
    print("Producer finished")


def main():
    with ProcessPoolExecutor() as executor:
        # Create Manager to grab a queue and an event
        manager = Manager()
        queue = manager.Queue()
        completed_event = manager.Event()

        # We can start multiple consumers if desired
        for i in range(1):
            executor.submit(consumer, i, queue, completed_event, )
        executor.submit(producer, queue, completed_event, )


if __name__ == "__main__":
    main()
