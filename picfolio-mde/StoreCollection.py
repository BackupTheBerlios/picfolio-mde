# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

import os.path
from Store import Store

class StoreCollection:
    def __init__(self):
        self.__stores = { }

    def __getdirname(self, f):
        if os.path.isdir(f):
            f = f + '/'
        dirname = os.path.dirname(f)
        if dirname == "":
            return "."
        else:
            return dirname

    def open(self, filename):
        dirname = self.__getdirname(filename)
        try:
            s = self.__stores[dirname]
        except KeyError:
            self.__stores[dirname] = Store(dirname)
            s = self.__stores[dirname]

    def get_item(self, filename, obj = None):
        store = self.getstore(filename)
        if obj != None:
            obj.store = store
        if os.path.isdir(filename):
            filename = None
        else:
            filename = os.path.basename(filename)
        return store.get_item(filename)

    def getstore(self, filename):
        try:
            store = self.__stores[self.__getdirname(filename)]
        except KeyError:
            self.open(filename)
            store = self.__stores[self.__getdirname(filename)]
        return store

    def is_dirty(self):
        for s in self.__stores:
            if self.__stores[s].is_dirty():
                return 1
        return 0

    def save(self, p):
        for s in self.__stores:
            self.__stores[s].save(p)
