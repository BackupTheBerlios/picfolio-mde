# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

class UI:
    def __init__ (self, stores):
        self.stores = stores
        self.store = None
        self.prevous_item = None

    def save_previous (self, item):
        self.previous_item = item

    def get_previous (self):
        return self.previous_item
