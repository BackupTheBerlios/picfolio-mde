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

    def __get_description_element(self):
        children = self.__node.childNodes
        for node in children:
            if node.nodeType != xml.dom.Node.ELEMENT_NODE or node.tagName != "description":
                continue
            return node
        return None

    def get_description(self, nonone = 0):
        desc_element = self.__get_description_element()
        if desc_element == None:
            value = None
        else:
            if not desc_element.hasChildNodes():
                value = ""
            else:
                for e in xmlutils.get_all_child_elements(desc_element):
                    if e.hasAttribute("xmlns"):
                        e.removeAttribute("xmlns")
                value = desc_element.toxml()
                value = re.sub("^<description>|</description>$", "",
                               value)
        if nonone and value == None:
            value = ""
        return value

    def string_to_description(self, value):
        s = "<description>" + value + "</description>"
        try:
            dom = parseString(s)
        except xml.parsers.expat.ExpatError:
            raise NotValid
        desc_element = dom.getElementsByTagName("description")[0]
        # Here, I am assuming that the content of the description element
        # is plain old XHTML; we have a namespace issue here; I need
        # to discuss that on the Picfolio mailing list
        # Setting the XHTML 1.0 namespace on all the elements
        for e in xmlutils.get_all_child_elements(desc_element):
            e.setAttribute("xmlns", "http://www.w3.org/1999/xhtml")
        return desc_element

    def set_description(self, value):
        if value == self.get_description():
            return
        desc_element = self.__get_description_element()
        if value != "":
            # Preparing element
            desc = self.string_to_description(value)
            if desc_element != None:
                self.__node.removeChild(desc_element)
            # Place it first
            if self.__node.hasChildNodes():
                self.__node.insertBefore(desc, self.__node.firstChild)
            else:
                self.__node.appendChild(desc)
        else:
            if desc_element != None:
                self.__node.removeChild(desc_element)
        self.__store.dirty()

class NotValid(Exception):
    """Data is not valid."""
    pass
