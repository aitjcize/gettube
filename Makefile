DESKTOP = debian/gettube.desktop
DESKTOP_PATH = /usr/share/applications
PY_COMPILE = ./py-compile
MSGFMT = msgfmt

TARGET = bin/gettube
BIN_PATH = /usr/bin

LIB_FILES = base/GetTubeBase.py\
	    base/GetTubeGui.py\
	    base/GetTubeConvert.py\
	    base/GetTubeMisc.py
PYTHON_LIB_PATH = /usr/lib/python2.6

PICS = images/gettube.png images/gettubebanner.png
PIXMAPS_PATH = /usr/share/pixmaps

PO = po
LOCALE_PATH = /usr/share/locale

compile:
	$(PY_COMPILE) $(LIB_FILES)
	@for p in `ls $(PO)/*.pot`; do $(MSGFMT) $$p -o $${p%pot}mo; done

install:
	cp -f $(DESKTOP) $(DESKTOP_PATH)
	cp -f $(LIB_FILES) base/*.pyc $(PYTHON_LIB_PATH)
	cp -f $(PICS) $(PIXMAPS_PATH)
	cp -f $(TARGET) $(BIN_PATH)
	@for p in `ls $(PO)/*.mo`; do\
		tmp=$${p%.mo};\
		cp -f $$p $(LOCALE_PATH)/$${tmp#po/}/LC_MESSAGES/gettube.mo;\
	done

clean:
	rm base/*.pyc base/*.pyo
	rm $(PO)/*.mo
