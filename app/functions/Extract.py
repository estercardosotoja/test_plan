from json import JSONDecodeError
import json as j
import json
from app.views import *
from django.shortcuts import render
from django.http import HttpResponse, Http404, QueryDict

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.http import FileResponse
from django.conf import settings
import os

from django.shortcuts import render

from jinja2 import Template


class Extract:

    def __init__(self, file):
        self.arq = file

    '''
        Retorna o titulo da especificação.
     '''
    def get_title(self):
        try:
            return self["info"]["title"]
        except KeyError:
            return print('Não há titulo')

    '''
        Retorna a versão da especificação.
     '''
    def get_version(self):
        try:
            return self["info"]["version"]
        except KeyError:
            return 'Não informado na especificação'

    '''
        Retorna a versão da especificação.
     '''
    def get_paths(self):
        try:
            return self.arq["paths"]
        except KeyError:
            return 'Não informado na especificação'

    '''
        Retorna a base_url da especificação.
     '''
    def get_base_url(self):
        try:
            host = self['host']
            path = self['basePath']
            return host+path
        except KeyError:
            return 'Não informado na especificação'

    """
        Verifica se há authorização na especficação 
    """
    def valid_autorization(self):
        try:
            context = { }
            if self['securityDefinitions']:
                autorizations = self['securityDefinitions']

                for auth, object_auth in autorizations.items():
                    self.valida_tipo_autorization(object_auth['type'])

                context = {
                    'name_auth': self['securityDefinitions'],
                    'type': 'aqui vai o o type do auth'
                }
                print(f'-------------------------------------------> Tem auth: {context}')
                return context
            else:
                print(f'Não tem auth')
                return 0
        except KeyError:
            return 'Não informado na especificação'

    '''
        Tipo de autorization
    '''
    def valida_tipo_autorization(string):
        if string == 'apiKey':
            print('Autorization = apiKey')
        elif string == 'basic':
            print('Autorization: basic')
        elif string == 'oauth2':
            print('Autorization: oauth2')
        else:
            print('Outro autorization')

