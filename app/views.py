import os
import json

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect

from app.forms import *
from django.shortcuts import render
from .forms import UploadFileForm


def index(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        print(f' URL: {context}')
    return render(request, "index.html", context)


def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'playload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'index.html')


def manual(request):
    return render(request, 'manual.html')


def contato(request):
    return render(request, 'contato.html')


def playload(request):
    return render(request, 'playload.html')


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
