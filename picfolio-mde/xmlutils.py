# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

import xml

# Has a Dom node a single child text node?
def hasChildTextNode(node):
    if node.hasChildNodes() and len(node.childNodes) == 1 and node.firstChild.nodeType == xml.dom.Node.TEXT_NODE:
        return 1
    else:
        return 0

# Get child text node
def getChildTextNode(node):
    if hasChildTextNode(node):
        return node.firstChild.data
    else:
        return None
