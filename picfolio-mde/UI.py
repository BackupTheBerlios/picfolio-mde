# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

class UI:
    def __init__ (self, store):
        self.store = store
        self.prevous_item = None

    def save_previous (self, item):
        self.previous_item = item

    def get_previous (self):
        return self.previous_item
