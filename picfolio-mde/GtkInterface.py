# Author: Hugo Haas <hugo@larve.net>
# License: GPLv2

from __future__ import division
import sys
import re
try:
    import gtk
    import gtk.glade
    has_gtk = 1
except:
    has_gtk = 0
from UI import UI
from Version import Version

# This should not depend on sys.argv[0]; GtkInterface could be used in lots
# of different ways @@@
GLADE_INTERFACE = re.sub("(/)?[^/]+$", "\\1picfolio-meta-data-editor.glade", sys.argv[0])

class GtkInterface(UI):

    def __init__ (self, store, pics):
        if has_gtk == 0:
            raise GtkUnavailable
        UI.__init__(self, store)
        self.gladexml = gtk.glade.XML(GLADE_INTERFACE)
        dic = { "on_quit1_activate" : self.quit,
                "on_quit_without_saving2_activate" : self.die,
                "on_save1_activate" : self.save_store,
                "on_main_destroy" : self.die,
                "on_SaveButton_clicked" : self.savenext,
                "on_SameButton_clicked" : self.samenext,
                "on_SkipButton_clicked" : self.next,
                "on_about1_activate" : self.about,
                "on_closebutton1_clicked" : self.about_close,
                }
        self.gladexml.signal_autoconnect(dic)
        self.status = self.gladexml.get_widget("Status")
        self.name = self.gladexml.get_widget("ImageName")
        self.title = self.gladexml.get_widget("TitleField")
        self.desc = self.gladexml.get_widget("DescriptionField")
        self.image = self.gladexml.get_widget("Image")
        self.saveButton= self.gladexml.get_widget("SaveButton")
        self.sameButton= self.gladexml.get_widget("SameButton")
        self.skipButton= self.gladexml.get_widget("SkipButton")
        self.aboutbox= self.gladexml.get_widget("AboutBox")
        self.progressBar = self.gladexml.get_widget("AnswerProgress")
        abouttitle = self.gladexml.get_widget("AboutTitle")
        abouttitle.set_label(re.sub("VERSION", Version.v, abouttitle.get_label()))
        self.args = pics
        if len(self.args) > 0:
            self.progress_step = 1.0 / len(self.args)
            self.show_picturedata(self.args[0])
            self.args = self.args[1:]
        else:
            self.error("No image specified")
            sys.exit(0)
        gtk.main()
        sys.exit(0)

    def about(self, obj):
        self.aboutbox.run()

    def about_close(self,obj):
        self.aboutbox.hide()

    def show_image(self):
        if self.pixbuf == None:
            return
        else:
            pb = self.pixbuf
        rect = self.image.get_allocation()
        area_ratio = rect.width / rect.height
        image_ratio = pb.get_width() / pb.get_height()
        if (area_ratio <= image_ratio):
            w = rect.width
            h = w / image_ratio
        else:
            h = rect.height
            w = h * image_ratio
        self.image.set_from_pixbuf(pb.scale_simple(int(w), int(h), gtk.gdk.INTERP_NEAREST))

    def show_picturedata(self, filename):
        self.filename = filename
        item = self.store.get_item(filename)
        if item == None:
            self.error("%s is not in %s" % filename, self.store.file())
        self.name.set_text(item.get_name())
        self.title.set_text(item.get_title(1))
        self.desc.set_text(item.get_description(1))
        self.title.grab_focus()
        if filename != None:
            self.pixbuf = gtk.gdk.pixbuf_new_from_file(item.get_name())
        else:
            self.pixbuf = None
        self.show_image()
        if len(self.args) == 1:
            self.saveButton.set_label("Save and quit")
            self.sameButton.set_label("Same and quit")
            self.skipButton.set_label("Skip and quit")
            self.progressBar.set_fraction(1)
        else:
            self.progressBar.set_fraction(self.progressBar.get_fraction() + self.progress_step)
        self.info("%s info loaded" % filename)

    def savenext(self, obj):
        item = self.store.get_item(self.filename)
        item.set_title(self.title.get_text())
        item.set_description(self.desc.get_text())
        self.next(obj)

    def samenext(self, obj):
        item = self.get_previous()
        self.title.set_text(item.get_title(1))
        self.desc.set_text(item.get_description(1))
        self.savenext(obj)

    def next(self, obj):
        item = self.store.get_item(self.filename)
        self.save_previous(item)
        if len(self.args) > 0:
            self.show_picturedata(self.args[0])
            self.args = self.args[1:]
        else:
            self.quit(obj)

    def save_store(self, obj):
        self.store.save(self.info)

    def status_show(self, context, str):
        cid = self.status.get_context_id(context)
        self.status.push(cid, str)
        
    def info(self, str):
        self.status_show("info", str)

    def error(self, str):
        self.status_show("error", str)

    def quit(self, obj):
        self.save_store(obj)
        self.close_ui(obj)

    def die(self, obj):
        # Confirm @@@
        self.close_ui(obj)

    def close_ui(self, obj):
        gtk.main_quit()
        sys.exit(0)

class GtkUnavailable(Exception):
    """GTK support is not available."""
    pass
