# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

import xml
import xmlutils

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
        # We assume that the description element is either:
        # <description>foo</description>
        # or:
        # <description><para>foo</para></description>
        # We return the first one which matches
        # There should be only one anyway
        children = self.__node.childNodes
        for node in children:
            if node.nodeType != xml.dom.Node.ELEMENT_NODE or node.tagName != "description":
                continue
            if node.hasChildNodes() and len(node.childNodes) == 1:
                if xmlutils.hasChildTextNode(node):
                    return node
                child = node.firstChild
                if child.nodeType == xml.dom.Node.ELEMENT_NODE and child.tagName == "para" and xmlutils.hasChildTextNode(child):
                    return node
            else:
                return node
        return None

    def get_description(self, nonone = 0):
        desc_element = self.__get_description_element()
        if desc_element != None:
            if desc_element.firstChild.nodeType == xml.dom.Node.ELEMENT_NODE:
                # para
                node = desc_element.firstChild
            else:
                # no para
                node = desc_element
            value = xmlutils.getChildTextNode(node)
        else:
            value = None
        if nonone and value == None:
            value = ""
        return value

    def set_description(self, value):
        if value == self.get_description():
            return
        desc_element = self.__get_description_element()
        if value != "":
            # Save a <description><para>foo</para></description>
            para = self.__store.dom.createElement("para")
            desctext = self.__store.dom.createTextNode(value)
            para.appendChild(desctext)
            if desc_element != None:
                # Replacing 
                desc_element.removeChild(desc_element.firstChild)
                desc_element.appendChild(para)
            else:
                desc = self.__store.dom.createElement("description")
                desc.appendChild(para)
                # Place it first
                if self.__node.hasChildNodes():
                    self.__node.insertBefore(desc, self.__node.firstChild)
                else:
                    self.__node.appendChild(desc)
        else:
            if desc_element != None:
                self.__node.removeChild(desc_element)
        self.__store.dirty()
