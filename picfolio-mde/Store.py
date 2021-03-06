# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

import xml
import os.path
from xml.dom.minidom import parse
from Item import Item
import sys

class Store:
    def __init__(self, dirname):
        self.__filename = dirname + '/picfolio/picfolio.xml'
        self.__dirname = os.path.abspath(dirname)
        self.__dirty = 0
        try:
            self.dom = parse(self.__filename)
        except IOError, e:
            print "Couldn't open %s: %s" % (self.__filename, e)
            print "Run picfolio first"
            sys.exit(1)
        self.__image_name_list = self.__get_image_list()

    def __get_image_list(self):
        list = [ ]
        for img in self.dom.getElementsByTagName("image"):
            list = list + [ img.getAttribute("name") ]
        return list

    def directory(self):
        return self.__dirname

    def get_item(self, filename):
        if (filename == None):
            return self.get_directory()
        else:
            return self.get_image(filename)

    def get_directory(self):
        return Item(self, self.dom.documentElement)

    def get_image(self, name):
        if name not in self.__image_name_list:
            return None
        else:
            for img in self.dom.getElementsByTagName("image"):
                if img.getAttribute("name") != name:
                    continue
                return Item(self, img)

    def file(self):
        return self.__filename

    def is_dirty(self):
        return self.__dirty

    def dirty(self):
        self.__dirty = 1

    def save(self, p):
        if self.__dirty:
            try:
                f = open(self.__filename, "w")
                f.write(self.dom.toxml())
                f.close()
                self.__dirty = 0
            except IOError, e:
                p("Couldn't write changes to %s: %s" % (self.__filename, e))
            p("Wrote changes to %s" % self.__filename)
        else:
            p("No save necessary")
        return
