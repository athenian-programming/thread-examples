from queue import Empty


class QueueContext(object):
    def __init__(self, queue, lock, completed):
        self.__queue = queue
        self.__lock = lock
        self.__completed = completed

    @property
    def completed(self):
        with self.__lock:
            return self.__completed.is_set() and self.__queue.qsize() == 0

    def mark_completed(self):
        self.__completed.set()

    def get_data(self):
        # Exit if the producer completed
        if self.completed:
            return None

        with self.__lock:
            # Read from the queue with get_nowait(), so we will get an Empty exception when we read
            # from an empty queue. This will prevent us from blocking after producer completion
            try:
                return self.__queue.get_nowait()
            except Empty:
                # Bail if no value is ready to be read
                return None

    def set_data(self, val):
        with self.__lock:
            # The queue will be full if the last item assigned has not already been read
            if self.__queue.full():
                # Empty the queue if item is already present
                discarded = self.__queue.get()
                print("Discarded {}".format(discarded))
            self.__queue.put(val)
