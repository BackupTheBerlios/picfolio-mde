# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

import xml

class Item:
    def __init__(self, store, node):
        self.__store = store
        self.__node = node

    def get_name(self):
        if self.__node.tagName == "directory":
            return self.__node.tagName
        elif self.__node.tagName == "image":
            return self.__node.getAttribute("name")
        else:
            raise UnknownElementError

    def get_title(self, nonone = 0):
        value = self.__node.getAttribute("title")
        if nonone and value == None:
            value = ""
        return value

    def set_title(self, value):
        if value == self.get_title():
            return
        if value == "":
            self.__node.removeAttribute("title")
        else:
            self.__node.setAttribute("title", value)
        self.__store.dirty()

    def __get_description_element(self):
        children = self.__node.childNodes
        for node in children:
            # Here I assume that description is a text node; I am not sure
            # it's a good assumption
            if node.nodeType == xml.dom.Node.ELEMENT_NODE and node.tagName == "description":
                return node
            else:
                return None
        return None

    def get_description(self, nonone = 0):
        desc_element = self.__get_description_element()
        if desc_element != None and desc_element.hasChildNodes() and desc_element.firstChild.nodeType == xml.dom.Node.TEXT_NODE:
            value = desc_element.firstChild.data
        else:
            value = None
        if nonone and value == None:
            value = ""
        return value

    def set_description(self, value):
        if value == self.get_description():
            return
        desc_element = self.__get_description_element()
        if desc_element == None:
            desc = self.__store.dom.createElement("description")
            desctext = self.__store.dom.createTextNode(value)
            desc.appendChild(desctext)
            if self.__node.firstChild:
                self.__node.insertBefore(desc, self.__node.firstChild)
            else:
                self.__node.appendChild(desc)
        else:
            if value != "":
                desc_element.firstChild.data = value
            else:
                self.__node.removeChild(desc_element)
        self.__store.dirty()
