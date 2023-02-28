from json import JSONDecodeError
import json as j
import json
from app.views import *
from django.shortcuts import render

from jinja2 import Template


class Extract:

    def __init__(self, file):
        self.arq = file

    def get_title(self):
        try:
            return self["info"]["title"]
        except KeyError:
            return print('Não há titulo')

    def get_version(self):
        try:
            return self["info"]["version"]
        except KeyError:
            return print('Não há version')

    def get_paths(self):
        try:
            return self.arq["paths"]
        except KeyError:
            return print('Não há titulo')
