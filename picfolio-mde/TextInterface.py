# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

from UI import UI

class TextInterface(UI):
    def enter_metadata(self, filename):
        item = self.store.get_item(filename)
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
        description = self.read("Description", item.get_description())
        if description != None:
            item.set_description(description)
        
    def read(self, prompt, text):
        try:
            import readline
            readline.add_history(text)
        except:
            pass
        try:
            input = raw_input(prompt + " > ")
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
