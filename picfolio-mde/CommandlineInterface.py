# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

from TextInterface import TextInterface

class CommandlineInterface(TextInterface):
    def enter_metadata(self, filename, has_title, title, has_desc, description):
        item = self.store.get_item(filename)
        if item == None:
            self.error("Skipping %s" % filename)
            return
        if has_title and title != None:
            self.info("Changing `%s' into `%s' for %s" % (item.get_title(), title, filename))
            item.set_title(title)
        if has_desc and description != None:
            self.info("Changing `%s' into `%s' for %s" % (item.get_description(), description, filename))
            item.set_description(description)
