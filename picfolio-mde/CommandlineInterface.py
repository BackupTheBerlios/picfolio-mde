# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

from TextInterface import TextInterface
from Item import NotValid

class CommandlineInterface(TextInterface):
    def enter_metadata(self, filename, has_title, title, has_desc, description):
        item = self.stores.get_item(filename, self)
        if item == None:
            self.error("Skipping %s" % filename)
            return
        if has_title and title != None:
            self.info("Changing `%s' into `%s' for %s" % (item.get_title(), title, filename))
            item.set_title(title)
        if has_desc and description != None:
            self.info("Changing `%s' into `%s' for %s" % (item.get_description(), description, filename))
            try:
                item.set_description(description)
            except NotValid:
                self.error("Data not valid; skipping")
