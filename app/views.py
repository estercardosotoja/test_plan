import os

from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def manual(request):
    return render(request, 'manual.html')


def contato(request):
    return render(request, 'contato.html')


def gerador(request):
    return render(request, 'gerador.html')


def download(request):
    return render(request, 'download.html')

