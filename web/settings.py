#! /usr/bin/env python
#-*- coding: utf-8 -*-

import os

DB_TYPE = 'sqlite'
DB_FILE = '../mycrawl/data.db'
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
SERVER_PORT = 9999
