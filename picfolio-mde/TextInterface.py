# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

from UI import UI
import sys
from Item import NotValid

class TextInterface(UI):
    def enter_metadata(self, filename):
        item = self.stores.get_item(filename, self)
        if item == None:
            self.error("%s is not in %s" % filename, self.store.file())
        self.show_properties(item)
        self.input_metadata(item)

    def show_properties(self, item):
        self.info("Information available for %s" % item.get_name())
        self.info("Title:\n  %s" % item.get_title())
        self.info("Description:\n  %s" % item.get_description())

    def input_metadata(self, item):
        self.info("Changing metadata for %s" % item.get_name())
        title = self.read("Title", item.get_title())
        if title != None:
            item.set_title(title)
        valid = 0
        while not valid:
            description = self.read("Description (XHTML 1.0)", item.get_description())
            if description != None:
                try:
                    item.set_description(description)
                except NotValid:
                    self.error("Data not valid")
                    valid = 0
                else:
                    valid = 1
        
    def read(self, prompt, text):
        try:
            import readline
            readline.add_history(text)
        except:
            pass
        try:
            input = raw_input(prompt + ":\n")
            # Enter == no changes
            if input == "":
                print "Keeping previous value"
                return None
            return input
        except EOFError:
            print "\nErasing value"
            # Ctrl-D == delete
            return ""
        except KeyboardInterrupt, e:
            print
            self.error("Ctrl-C... quitting without saving")
            sys.exit(2)

    def info(self, str):
        print "-=- %s" % str

    def error(self, str):
        print "ERROR: %s" % str

    def debug_out(self, str):
        print "*** %s" % str
