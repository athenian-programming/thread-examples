#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread


def print_names(name):
    for i in range(10):
        print("{0} says hello {1}".format(name, i))


def main():
    Thread(target=print_names, args=("Bob",)).start()
    Thread(target=print_names, args=("Bill",)).start()
    Thread(target=print_names, args=("Mary",)).start()


if __name__ == "__main__":
    main()
