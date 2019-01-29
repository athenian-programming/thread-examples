from queue import Empty


class QueueContext(object):
    def __init__(self, queue, completed):
        self.__queue = queue
        self.__completed = completed

    @property
    def completed(self):
        return self.__completed.is_set() and self.__queue.qsize() == 0

    def mark_completed(self):
        self.__completed.set()

    def get_data(self):
        # Exit if the producer completed
        if self.completed:
            return None

        try:
            return self.__queue.get(block=True, timeout=.5)
        except Empty:
            # Bail if no value is ready to be read
            return None

    def set_data(self, val):
        self.__queue.put(val)
