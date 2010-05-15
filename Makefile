INSTALL_PATH = /usr/share/gettube
DESKTOP = debian/gettube.desktop
DESKTOP_PATH = /usr/share/applications
PY_COMPILE = ./py-compile
MSGFMT = msgfmt

TARGET = bin/gettube
BIN_PATH = /usr/bin

LIB_FILES = gettube

PYTHON_LIB_PATH = /usr/lib/python2.6

ICON = images/gettube.png
PIXMAPS_PATH = /usr/share/pixmaps

IMAGES = images/gettube.png images/gettubebanner.png
IMAGES_PATH = $(INSTALL_PATH)/images

PO = po
LOCALE_PATH = /usr/share/locale

MISC = AUTHORS COPYING README

compile:
	$(PY_COMPILE) `find $(LIB_FILES) -name *.py`
	@for p in `ls $(PO)/*.pot`; do $(MSGFMT) $$p -o $${p%pot}mo; done

install:
	mkdir -p $(INSTALL_PATH)
	mkdir -p $(IMAGES_PATH)
	cp -f $(DESKTOP) $(DESKTOP_PATH)
	cp -rf $(LIB_FILES) $(INSTALL_PATH)
	cp -f $(IMAGES) $(IMAGES_PATH)
	cp -f $(ICON) $(PIXMAPS_PATH)
	cp -f $(TARGET) $(BIN_PATH)
	cp -f $(MISC) $(INSTALL_PATH)
	@for p in `ls $(PO)/*.mo`; do\
		tmp=$${p%.mo};\
		cp -f $$p $(LOCALE_PATH)/$${tmp#po/}/LC_MESSAGES/gettube.mo;\
	done

clean:
	rm `find $(LIB_FILES) -name *.pyc`
	rm $(PO)/*.mo

gettext:
	pygettext bin/gettube `find -name '*.py'`
	mv messages.pot po
