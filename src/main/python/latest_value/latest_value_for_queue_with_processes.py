#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ProcessPoolExecutor
from latest_value.queue_context import QueueContext
from multiprocessing import Manager
from random import randrange


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
    # Create a Manager
    manager = Manager()
    # Set the maximum size of the Queue to be 1
    queue = manager.Queue(maxsize=1)
    lock = manager.Lock()
    completed = manager.Event()
    context = QueueContext(queue, lock, completed)

    with ProcessPoolExecutor() as executor:
        executor.submit(consumer, context, )
        executor.submit(producer, context, count, )


if __name__ == "__main__":
    main()
