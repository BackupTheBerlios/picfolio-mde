# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

import xml
import xmlutils
from xml.dom.minidom import parseString
import re

class Item:
    def __init__(self, store, node):
        self.__store = store
        self.__node = node

    def isdir(self):
        if self.__node.tagName == "directory":
            return 1
        else:
            return 0
            
    def get_name(self):
        if self.isdir():
            return self.get_fullname()
        elif self.__node.tagName == "image":
            return self.__node.getAttribute("name")
        else:
            raise UnknownElementError

    def get_fullname(self):
        if self.isdir():
            return self.__store.directory()
        else:
            return self.__store.directory() + '/' + self.get_name()

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

    def __get_description_element(self, simple = 1):
        children = self.__node.childNodes
        for node in children:
            if node.nodeType != xml.dom.Node.ELEMENT_NODE or node.tagName != "description":
                continue
            if not simple:
                return node
            # We assume that the description element is either:
            # <description>foo</description>
            # or:
            # <description><para>foo</para></description>
            if node.hasChildNodes() and len(node.childNodes) == 1:
                if xmlutils.hasChildTextNode(node):
                    return node
                child = node.firstChild
                if child.nodeType == xml.dom.Node.ELEMENT_NODE and child.tagName == "para" and xmlutils.hasChildTextNode(child):
                    return node
            else:
                return node
        return None

    def get_description(self, nonone = 0, markup = 0):
        desc_element = self.__get_description_element(not markup)
        if desc_element == None:
            value = None
        elif markup:
            if not desc_element.hasChildNodes():
                value = ""
            else:
                value = desc_element.toxml()
                value = re.sub("^<description>|</description>$", "",
                               value)
        elif desc_element.hasChildNodes():
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

    def string_to_description(self, value):
        s = "<description>" + value + "</description>"
        dom = parseString(s)
        desc_element = dom.getElementsByTagName("description")[0]
        return desc_element

    def set_description(self, value, markup = 0):
        if value == self.get_description():
            return
        desc_element = self.__get_description_element(markup)
        if value != "":
            # Preparing element
            new_desc = None
            if markup:
                new_desc = self.string_to_description(value)
            else:
                # Creating: <description><para>foo</para></description>
                new_desc = self.__store.dom.createElement("para")
                desctext = self.__store.dom.createTextNode(value)
                new_desc.appendChild(desctext)
            # Inserting data
            if not markup and desc_element != None:
                # Replacing 
                desc_element.removeChild(desc_element.firstChild)
                desc_element.appendChild(new_desc)
            else:
                desc = None
                if markup:
                    if desc_element != None:
                        self.__node.removeChild(desc_element)
                    desc = new_desc
                else:
                    desc = self.__store.dom.createElement("description")
                    desc.appendChild(new_desc)
                # Place it first
                if self.__node.hasChildNodes():
                    self.__node.insertBefore(desc, self.__node.firstChild)
                else:
                    self.__node.appendChild(desc)
        else:
            if desc_element != None:
                self.__node.removeChild(desc_element)
        self.__store.dirty()
