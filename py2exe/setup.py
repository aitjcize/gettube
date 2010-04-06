# setup.py
from distutils.core import setup
import py2exe
import gobject
import cairo

setup(
    name = "GetTube",
    description = "Download YouTube video easily",
    version = "0.5.3",
    windows = [
        {
            "script": "GetTube.py",
            "icon_resources": [(1, "gettube.ico")]
        }
    ],
    data_files=[("gettube.png")]
)

