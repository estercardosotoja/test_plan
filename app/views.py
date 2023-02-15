from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect

from app.forms import *
from app.functions.Readfiles import *
from django.shortcuts import render
from .forms import UploadFileForm


from django.core.files.storage import FileSystemStorage
from app.functions.Readfiles import *
from django.shortcuts import render
from app.functions.Genaretor import *


def index(request):
    context = {}
    if request.method == 'POST':
        if request.FILES.get('document', False):
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            path = ReadFile(uploaded_file.name)
            result = path.open_file()
            if result == 0:
                context = alert('Revise o arquivo, sintaxe errada!')
                return render(request, "index.html", context)
            else:
                context = {
                    'name': name,
                    'spec': result
                }

                html_generator = Extract(context['spec'])
                html_entrada = html_generator.generate()

                with open("../projeto_tecnologico/templates/checkbox.html", "w") as file:
                    file.write(html_entrada)

                return render(request, "gerador.html", context)
        else:
            context = alert('Selecione uma arquivo para realizar o upload!')
            return render(request, "index.html", context)
    else:
        return render(request, "index.html")


def gerador(request, context):
    arq = Extract(context['name'])
    print(context['name'])
    path = arq.get_paths()
    text = {
        'path': path
    }
    return render(request, 'gerador.html', text)


def manual(request):
    return render(request, 'manual.html')


def contato(request):
    return render(request, 'contato.html')

def download(request):
    return render(request, 'download.html')


def alert(msg):
    context = {
        'msg': True,
        'text': msg
    }
    return context
