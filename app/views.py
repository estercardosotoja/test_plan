import tempfile
import os
import tempfile

from django.http import HttpResponse, Http404, QueryDict

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.http import FileResponse
from django.conf import settings
import os

from django.shortcuts import render

from app.functions.Extract import Extract
from app.functions.Extract import *
from .functions.Readfiles import ReadFile
from .functions.GeneratorPDF import *
from static.js import *

infos_file_spec = None
ordem_imprimir = None


def set_infos_file_spec(value):
    global infos_file_spec
    infos_file_spec = value


def get_infos_file_spec():
    return infos_file_spec


def set_ordem_imprimir(value):
    global ordem_imprimir
    ordem_imprimir = value


def get_ordem_imprimir():
    return ordem_imprimir


def index(request):
    context = {}
    try:
        # Valida que há um envio do formulário do arquivo
        if request.method == 'POST':
            # Valida que há um arquivo importado na requisição
            if request.FILES.get('document', False):
                uploaded_file = request.FILES['document']
                fs = FileSystemStorage()
                name = fs.save(uploaded_file.name, uploaded_file)
                path = ReadFile(uploaded_file.name)

                # Valida se o arquivo é um Json e Yaml e está na sintaxe correta
                result = path.open_file()
                if result == 0:
                    context = alert('Revise o arquivo, sintaxe errada!')
                    return render(request, "index.html", context)

                # valida se o arquivo é uma especificação da Open API
                ehspec = valida_existencia_path(result)
                if ehspec == 0:
                    context = alert('Selecione um arquivo de especificação conforme a OPEN API para realizar o upload!')
                    return render(request, "index.html", context)
                else:
                    infos_arq_spec = {
                        'name': name,
                        'spec': result
                    }
                    set_infos_file_spec(infos_arq_spec)
                    context = infos_spec(infos_arq_spec)
                    print(context)
                    return render(request, "../templates/generator_form.html", context)

            else:
                context = alert('Selecione um arquivo para realizar o upload!')
                return render(request, "index.html", context)
        else:
            return render(request, "index.html")
    except HttpResponseNotFound:
        context = alert('Algo de errado ao acessar a página, tente mais tarde!')
        return render(request, "index.html", context)
    except TypeError:
        context = alert('Arquivo de extensão Inválida!')
        return render(request, "index.html", context)


def generator(request, context):
    try:
        return render(request, "generator_form.html", context)
    except TypeError:
        context = alert('Arquivo de extensão Inválida!')
        return render(request, "index.html", context)


def confirm(request):
    try:
        if request.method == 'POST':
            if 'download' in request.POST:
                return render(request, '../templates/dynamic/download.html')
            else:

                ordem_request = request.POST.getlist('ordem')
                paths_verbs_all = paths_verbs_cmp(get_infos_file_spec())

                ordem_para_imprimir = tipos_dos_campos_paths_verbs_cmps(paths_verbs_all, ordem_request)
                # print('Ordem para imprimir:', ordem_para_imprimir)
                set_ordem_imprimir(ordem_para_imprimir)

                context = {
                    'ordem_para_imprimir': ordem_para_imprimir
                }
                # print('Ordem para imprimir:', ordem_para_imprimir)
                return render(request, '../templates/confirm.html', context)
        else:
            context = alert('Algo de errado aconteceu! Recebemos outro metódo HTTP - POST')
            return render(request, '../templates/index.html', context)
    except TypeError:
        context = alert('Erro ao intepretar as tags do arquivo! Tente novamente')
        return render(request, '../templates/index.html', context)


def download(request):
    try:
        if request.method == 'POST':
            if 'downloaded' in request.POST:
                return render(request, '../templates/downloaded.html')
            else:
                context = {
                    'dados': get_ordem_imprimir()
                }

                arq = GeneratorPDF.Gerar(get_ordem_imprimir())
                return render(request, '../templates/download.html', context=context)
        else:
            return render(request, '../templates/index.html',
                          context=alert('Algo de errado aconteceu! Recebemos outro metódo HTTP!'))
    except TypeError:
        return render(request, '../templates/confirm.html', context=alert('Algo de errado aconteceu : TypeError!'))
    except FileNotFoundError:
        raise Http404("O arquivo não existe")


def downloaded(request):
    try:
        if request.method == 'POST':
            return render(request, "downloaded.html")
    except FileNotFoundError:
        return HttpResponseNotFound()


def manual(request):
    return render(request, 'manual.html')


def contato(request):
    return render(request, 'contato.html')


def alert(msg):
    context = {
        'msg': True,
        'text': msg
    }
    return context


def infos_spec(spec):
    html_generator = Extract(spec['spec'])
    html_entrada = html_generator.get_paths()
    title_api = Extract.get_title(spec['spec'])
    version_api = Extract.get_version(spec['spec'])
    host = Extract.get_base_url(spec['spec'])
    context = {
        'name': spec['name'],
        'spec': spec['spec'],
        'paths': html_entrada,
        'title': title_api,
        'version': version_api,
        'host_base_path': host
    }
    return context


def dados_separados(paths):
    context = {}
    all_paths = []
    all_verbs = []
    all_cmp = []

    for path, path_object in paths.items():
        all_paths.append(path)
        for verb, verb_object in path_object.items():
            all_verbs.append(verb)
            if not isinstance(verb_object, dict):
                # print(f"Esperava um objeto do tipo 'dict' para o verbo {verb}, mas recebeu {type(verb_object)}")
                continue
            parameters = verb_object.get('parameters')
            if not isinstance(parameters, (list, tuple)):
                # print(f"Esperava uma lista ou tupla de parâmetros para o verbo {verb}, mas recebeu {type(parameters)}")
                continue
            for parameter in parameters:
                all_cmp.append(parameter['name'])
                if parameter.get('required'):
                    print('Campo obrigatório')
                else:
                    print('Campo opcional')

    context = {
        'all_paths': all_paths,
        'all_verbs': all_verbs,
        'all_cmp': all_cmp
    }

    return context


def paths_verbs_cmp(spec):
    dados_gerais = infos_spec(spec)
    separados_geral = dados_gerais['paths']
    separado_paths = dados_separados(separados_geral)

    return separado_paths


def verifica_path(paths, item):
   # print('PATHS: ', paths)
    for path in paths:
    #    print(path, '==', item)
        if path == item:
            return item


def verifica_verbs(verbs, item):
    # print('VERBS: ', verbs)
    for verb in verbs:
        # print(verb, '==', item)
        if verb == item:
            return item


def verifica_cmp(cmps, item):
    # print('CMPS: ', cmps)
    for cmp in cmps:
        #  print(cmp, '==', item)
        if cmp == item:
            return item


def tipos_dos_campos_paths_verbs_cmps(paths_verbs_all, ordem_request):
    ordem_para_imprimir = {}

    paths = paths_verbs_all['all_paths']
    verbs = paths_verbs_all['all_verbs']
    cmps = paths_verbs_all['all_cmp']

    for item in ordem_request:
        if verifica_path(paths, item) is not None:
            path = {item: 'path'}
            ordem_para_imprimir.update(path)
        elif verifica_verbs(verbs, item) is not None:
            verb = {item: 'verb'}
            ordem_para_imprimir.update(verb)
        elif verifica_cmp(cmps, item) is not None:
            cmp = {item: 'cpm'}
            ordem_para_imprimir.update(cmp)
        else:
           print(f'Vish né nada não', item)

    return ordem_para_imprimir


def valida_existencia_path(spec):
    retorno = 0
    for item in spec.keys():
        if item == 'paths':
            if len(item) > 0:
                retorno = 1

    return retorno
