# GetTube Makefile

PY_COMPILE = ./py-compile
MSGFMT = msgfmt

INSTALL_PATH = /usr/share/gettube

DESKTOP = debian/gettube.desktop
DESKTOP_PATH = /usr/share/applications

TARGET = bin/gettube
BIN_PATH = /usr/bin

LIB_FILES = gettube
LIB_PATH = /usr/lib/gettube

ICON = images/gettube.png
PIXMAPS_PATH = /usr/share/pixmaps

IMAGES = images/gettube.png images/gettubebanner.png
IMAGES_PATH = $(INSTALL_PATH)/images

PO = po
LOCALE_PATH = /usr/share/locale

MISC = AUTHORS COPYING README

compile:
	$(PY_COMPILE) `find $(LIB_FILES) -name *.py`
	@for p in `ls $(PO)/*.po`; do $(MSGFMT) $$p -o $${p%po}mo; done

install:
	# Create necessary path
	mkdir -p $(INSTALL_PATH)
	mkdir -p $(LIB_PATH)
	mkdir -p $(IMAGES_PATH)

	# Copy gettube.desktop
	cp -f $(DESKTOP) $(DESKTOP_PATH)

	# Copy gettube python package
	cp -rf $(LIB_FILES) $(LIB_PATH)

	# Copy Images
	cp -f $(IMAGES) $(IMAGES_PATH)

	# Copy Icon
	cp -f $(ICON) $(PIXMAPS_PATH)

	# Copy Binary executalbe
	cp -f $(TARGET) $(BIN_PATH)

	# Copy Misc.
	cp -f $(MISC) $(INSTALL_PATH)
	@for p in `ls $(PO)/*.mo`; do\
		tmp=$${p%.mo};\
		cp -f $$p $(LOCALE_PATH)/$${tmp#po/}/LC_MESSAGES/gettube.mo;\
	done

clean:
	rm `find $(LIB_FILES) -name *.pyc`
	rm $(PO)/*.mo

gettext:
	xgettext -L python bin/gettube `find -name '*.py'`
	mv messages.po po
