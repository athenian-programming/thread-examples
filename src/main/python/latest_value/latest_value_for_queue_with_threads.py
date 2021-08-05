#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from latest_value.queue_context import QueueContext
from queue import Queue
from random import randrange
from threading import Event
from threading import Lock


def consumer(context):
    while not context.completed:
        data = context.get_data()
        if data is not None:
            print("Consumed {}".format(data))
        # Pause a random amount of time
        time.sleep(randrange(3))
    print("Consumer finished")


def producer(context, count):
    for i in range(count):
        data = "image-{0}".format(i)
        context.set_data(data)
        print("Put {}".format(data))
        # Pause a random amount of time
        time.sleep(randrange(2))
    context.mark_completed()
    print("Producer finished")


def main():
    count = 10
    # Set the maximum size of the Queue to be 1
    queue = Queue(maxsize=1)
    lock = Lock()
    completed = Event()
    context = QueueContext(queue, lock, completed)

    with ThreadPoolExecutor() as executor:
        executor.submit(consumer, context, )
        executor.submit(producer, context, count, )


if __name__ == "__main__":
    main()
