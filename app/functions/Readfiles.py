import json as j
import os
from json import JSONDecodeError

import yaml


class ReadFile:

    def __init__(self, arq):
        self.path = f'media/{arq}'

    '''
        Valida qual o tipo de extensão do arquivo.
    '''
    def json_or_yaml(self):
        try:
            name_file, extensao = os.path.splitext(self.path)
            if extensao == '.json':
                return 1
            elif extensao == '.yaml':
                return 2
            else:
                print("\n Arquivo de outro formato")
                return 0
        except FileNotFoundError:
            print('\n Erro ao identificar extensão do arquivo')
            return 0
    '''
        Abre o arquivo de extensão YAML retornando o conteúdo.
    '''
    def open_file_yaml(self):
        try:
            with open(self.path, 'r') as arq:
                arq_yaml = yaml.full_load(arq)
                return arq_yaml
        except FileNotFoundError:
            print('\n Erro ao abrir o arquivo')
            return 0
        except TypeError:
            print('\n Erro ao abrir o arquivo')
            return 0
        except BaseException:
            print('\n Erro ao abrir o arquivo')
            return 0

    '''
        Abre o arquivo de extensão JSON retornando o conteúdo.
    '''
    def open_file_json(self):
        try:
            with open(self.path, 'r') as arq:
                arq_json = j.load(arq)
                return arq_json
        except FileNotFoundError:
            print('\n Erro ao abrir o arquivo')
            return 0
        except JSONDecodeError:
            print('\n Erro ao abrir o arquivo')
            return 0
        except TypeError:
            print('\n Erro ao abrir o arquivo')
            return 0
        except BaseException:
            print('\n Erro ao abrir o arquivo')
            return 0


    '''
        Valida qual a extensão chamando o metodos que extraem o 
        conteúdo do arquivo confome a extensão e retorna o 
        conteúdo extraído do arquivo.
    '''
    def open_file(self):

        try:
            type = self.json_or_yaml()
            if type == 1:
                arq = self.open_file_json()
                return arq
            elif type == 2:
                arq = self.open_file_yaml()
                return arq
            else:
                return 0
        except FileNotFoundError:
            print('\n Erro ao chamar as funções para abrir os arquivos')
            return 0
        except JSONDecodeError:
            print('\n Erro ao abrir o arquivo')
            return 0
