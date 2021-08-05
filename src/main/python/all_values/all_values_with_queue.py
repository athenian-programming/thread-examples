#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from all_values.queue_context import QueueContext
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from random import randrange
from threading import Event


def consumer(id, context):
    while not context.completed:
        data = context.get_data()
        if data is not None:
            print("Consumer {} got {}".format(id, data))
        # Pause a random amount of time
        time.sleep(randrange(2))
    print("Consumer finished")


def producer(context, count):
    for i in range(count):
        data = "val-{0}".format(i)
        print("Producer put {}".format(data))
        context.set_data(data)
        # Pause a random amount of time
        time.sleep(randrange(2))
    context.mark_completed()
    print("Producer finished")


def main():
    count = 10
    queue = Queue()
    completed = Event()
    context = QueueContext(queue, completed)

    with ThreadPoolExecutor() as executor:
        # Can launch an arbitrary number of consumer threads
        for i in range(3):
            executor.submit(consumer, i, context, )
        executor.submit(producer, context, count, )


if __name__ == "__main__":
    main()
