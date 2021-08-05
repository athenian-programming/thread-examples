#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from all_values.queue_context import QueueContext
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from queue import Empty
from random import randrange


def consumer(id, context):
    while not context.completed:
        print("Waiting on id: {}".format(id))
        try:
            data = context.get_data()
            print("Consumer {} got {}".format(id, data))
        except Empty:
            continue
    print("Consumer finished")


def producer(context, count):
    for i in range(count):
        data = "val-{}".format(i)
        print("Producer put {}".format(data))
        context.set_data(data)
        time.sleep(randrange(2))
    context.mark_completed()
    print("Producer finished")


def main():
    count = 10
    # Create Manager
    manager = Manager()
    queue = manager.Queue()
    completed = manager.Event()
    context = QueueContext(queue, completed)

    with ProcessPoolExecutor() as executor:
        # Can launch an arbitrary number of consumer processes
        for i in range(1):
            executor.submit(consumer, i, context, )
        executor.submit(producer, context, count, )


if __name__ == "__main__":
    main()
