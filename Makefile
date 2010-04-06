DESKTOP = gettube.desktop
DESKTOP_PATH = /usr/share/applications
PY_COMPILE = ./py-compile
MSGFMT = msgfmt

TARGET = bin/gettube
BIN_PATH = /usr/bin

LIB_FILES = base/GetTubeBase.py\
	    base/GetTubeGui.py\
	    base/GetTubeConvert.py\
	    base/Misc.py
PYTHON_LIB_PATH = /usr/lib/python2.6

LOGO = images/gettube.png
PIXMAPS_PATH = /usr/share/pixmaps

TRANSLATION = translations/gettube.mo
LOCALE_PATH = /usr/share/locale/zh_TW/LC_MESSAGES

compile:
	$(PY_COMPILE) $(LIB_FILES)
	$(MSGFMT) translations/gettube.pot -o $(TRANSLATION)

install:
	cp -f $(DESKTOP) $(DESKTOP_PATH)
	cp -f $(LIB_FILES) base/*.pyc $(PYTHON_LIB_PATH)
	cp -f $(LOGO) $(PIXMAPS_PATH)
	cp -f $(TARGET) $(BIN_PATH)
	cp -f $(TRANSLATION) $(LOCALE_PATH)

clean:
	rm base/*.pyc base/*.pyo
	rm $(TRANSLATION)
