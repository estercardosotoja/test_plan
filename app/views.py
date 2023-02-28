from django.core.files.storage import FileSystemStorage

from app.functions.Extract import Extract
from app.functions.Extract import *
from .functions.Readfiles import ReadFile


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
                html_entrada = html_generator.get_paths()
                title_api = Extract.get_title(context['spec'])
                version_api = Extract.get_version(context['spec'])

                # with open("../projeto_tecnologico/templates/dynamic/checkbox.html", "w") as file:
                # file.write(html_entrada)
                context = {
                    'name': name,
                    'spec': result,
                    'paths': html_entrada,
                    'title': title_api,
                    'version': version_api
                }
                return render(request, "../templates/partials/_generator_form.html", context)
        else:
            context = alert('Selecione uma arquivo para realizar o upload!')
            return render(request, "index.html", context)
    else:
        return render(request, "index.html")


def gerador(request, context):
    return render(request, "/partials/_generator_form.html", context)


"""

def saida(request):
    if request.method == 'POST':
        opcoes_selecionadas = request.POST.getlist('opcoes')
        # faça algo com as opções selecionadas
        # exiba o template do formulário
        context = {'opcoes': opcoes_selecionadas}
        return render(request, '../templates/dynamic/out.html', context)
    else:
        opcoes_selecionadas = 'ERROR'
        context = {'opcoes': opcoes_selecionadas}
    return render(request, '/templates/dynamic/out.html', context)
"""


def saida(request):
    if request.method == 'POST':
        selected_paths = request.POST.getlist('path')
        selected_verbs = request.POST.getlist('verb')
        print(f'\n verbs: {selected_verbs}')
        print(f'\n path: {selected_paths}')

        context = {
            'selected_verbs': selected_verbs,
            'selected_paths': selected_paths
        }
        return render(request, '../templates/dynamic/out.html', context)
    else:
        context = {
            'MSG': 'ERROR'
        }
        print(context)
        return render(request, '../templates/dynamic/out.html', context)

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
