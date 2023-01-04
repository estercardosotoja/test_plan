from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect

from app.forms import *
from app.functions.Readfiles import *
from django.shortcuts import render
from .forms import UploadFileForm


from django.core.files.storage import FileSystemStorage
from app.functions.Readfiles import *
from django.shortcuts import render


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
                return render(request, "playload.html", context)
        else:
            context = alert('Selecione uma arquivo para realizar o upload!')
            return render(request, "index.html", context)
    else:
        return render(request, "index.html")



def playload(request):
    return render(request, 'playload.html')


def manual(request):
    return render(request, 'manual.html')


def contato(request):
    return render(request, 'contato.html')


def gerador(request):
    dados_tests = {
        1: "POST",
        2: "GET",
        3: "PUT",
        4: "DELETE",
        5: "POST",
        6: "GET",
    }
    dados = {
        'testes': dados_tests
    }
    return render(request, 'gerador.html', dados)


def download(request):
    return render(request, 'download.html')


def alert(msg):
    context = {
        'msg': True,
        'text': msg
    }
    return context
