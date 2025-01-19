# PythonAnyware

import sys
import os

project_home = '/home/std66122420120/cwad'
os.chdir(project_home)
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from api import config
config.IS_SERVERLESS = False

from api import app as application
