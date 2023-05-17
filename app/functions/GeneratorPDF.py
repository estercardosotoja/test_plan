from reportlab import pdfbase
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph


class GeneratorPDF:
    altura = None

    """
        Gera o PDF
    """

    def Gerar(spec, context):
        set_altura(700)
        # Intanciar arquivo
        name_pdf = "testplan"
        diretorio = "media/testplan/"
        caminho_completo = diretorio + name_pdf
        pdf = canvas.Canvas('{}.pdf'.format(caminho_completo), pagesize=A4)

        # Itera intens selecionados para teste

        # Logo
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawImage("setup/static/img/logo.png", 15, 755, width=160, height=80)

        # Titulo: Plano de Testes de API
        title_header(pdf, spec)

        # Sub-titulo: Plano de Testes de API
        sub_title_header(pdf, spec)

        # Detalhes
        description_header(pdf, spec)

        # Version
        version_header(pdf, spec)

        # Host
        host_header(pdf, spec)

        # Base
        base_header(pdf, spec)

        # Items
        title_items(pdf)

        # Todos Items
        todos_os_items(pdf, spec)

        # Title Testes
        title_Testes(pdf)

        # Montando os Testes
        montando_testes(pdf, context, spec)

        # Titulo/Nome do serviço
        pdf.save()
        print('{}.pdf criado com sucesso!'.format(name_pdf))
        return 1


"""
    Variavel que define a posição dos elementos no PDF
"""


def set_altura(value):
    global altura
    altura = value


"""
    Variavel que retorna a posição dos elementos no PDF
"""


def get_altura():
    return altura


"""
  Titulo do Arquivo: Plano de Testes de API
"""


def title_header(pdf, spec):
    try:
        if spec['spec']['info']['title'] is True:
            pdf.setFont("Helvetica-Bold", 24)
            title = spec['spec']['info']['title']
            pdf.drawString(180, 775, title)
        else:
            pdf.setFont("Helvetica-Bold", 24)
            pdf.drawString(180, 775, "Teste de API")
    except TypeError:
        print("Erro na função 'title_header' no GeneratorPDF")


"""
  Subtitulo: 
"""


def sub_title_header(pdf, spec):
    try:
        if spec['spec']['info']['title'] is True:
            sub_titulo = spec['spec']['info']['title']
            pdf.setFont("Helvetica-Oblique", 16)
            pdf.drawString(225, 740, sub_titulo)
        else:
            pdf.setFont("Helvetica-Oblique", 16)
            pdf.drawString(225, 740, 'Application Programming Interface ')
    except TypeError:
        print("Erro na função 'sub_title_header' no GeneratorPDF")


"""
  Descrição da aplicação:
"""


def description_header(pdf, spec):
    try:
        if spec['spec']['info']['title'] is True:
            description = spec['spec']['info']['description']
            pdf.setFont("Helvetica-Oblique", 10)
            pdf.drawString(30, 720, f'Description: {description}')
        else:
            pdf.setFont("Helvetica-Oblique", 10)
            pdf.drawString(30, 720, 'Description: Não informado')
    except TypeError:
        print("Erro na função 'description_header' no GeneratorPDF")


"""
  Version:
"""


def version_header(pdf, spec):
    try:
        if spec['spec']['info']['version'] is True:
            version = spec['spec']['info']['version']
            pdf.setFont("Helvetica-Oblique", 10)
            pdf.drawString(30, 700, f' Version: {version}')
        else:
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(30, 700, "Version: Não informado")
    except KeyError:
        print("Erro na função 'host_header' no GeneratorPDF")



"""
  Host:
"""


def host_header(pdf, spec):
    try:
        if spec['spec']['host'] is True:
            host = spec['spec']['host']
            pdf.setFont("Helvetica-Oblique", 10)
            pdf.drawString(200, 700, f'Host: {host}')
        else:
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(200, 700,  "Host: Não informado")
    except KeyError:
        print("Erro na função 'host_header' no GeneratorPDF")


"""
  Base:
"""


def base_header(pdf, spec):
    try:
        if spec['spec']['basePath'] is True:
            base = spec['spec']['basePath']
            pdf.setFont("Helvetica-Oblique", 10)
            pdf.drawString(450, 700, f'basePath: {base}')
        else:
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(450, 700, f'basePath: Não informado')
    except KeyError:
        print("Erro na função 'host_header' no GeneratorPDF")


"""
  Title: ITEMS
"""


def title_items(pdf):
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, 670, "Items")
    pdf.setLineWidth(1)
    pdf.line(30, 650, 550, 650)


"""
  Title: ITEMS
"""


def items_text(pdf, spec, item, value):
    set_altura(new_page(pdf, 10, spec))
    subtitle_items(pdf, item, value, spec)


"""
  Monta um dict com todos os itens da specificação para listar os items
"""


def todos_os_items(pdf, spec):
    set_altura(650)
    testes = {}
    id = 0
    for path, path_object in spec['spec']['paths'].items():
        id = id + 1
        testes.update({f'path{id}': path})
        items_text(pdf, spec, f'path{id}', path)
        for verb, verb_object in path_object.items():
            id = id + 1
            testes.update({f'verb{id}': verb})
            items_text(pdf, spec, f'verb{id}', verb)
            if 'parameters' in verb_object:
                for parameter in verb_object['parameters']:
                    if parameter.get("type") is not None and parameter.get('required') is not None:
                        id = id + 1
                        if not parameter.get('required'):
                            tipo_campo = "Opcional"
                            testes.update(
                                {f'parameter{id}': f"{parameter['name']} - {parameter['type']} - Campo {tipo_campo}"})
                            items_text(pdf, spec, f'parameter{id}',
                                       f"{parameter['name']} - {parameter['type']} - Campo {tipo_campo}")
                        else:
                            tipo_campo = "Obrigatório"
                            testes.update(
                                {f'parameter{id}': f"{parameter['name']} - {parameter['type']} - Campo {tipo_campo}"})
                            items_text(pdf, spec, f'parameter{id}',
                                       f"{parameter['name']} - {parameter['type']} - Campo {tipo_campo}")
                    elif parameter.get("type") is not None:
                        id = id + 1
                        testes.update({f'parameter{id}': f"{parameter['name']} - {parameter['type']}"})
                        items_text(pdf, spec, f'parameter{id}', f"{parameter['name']} - {parameter['type']}")
                    elif parameter.get("required") is not None:
                        testes.update({f'parameter{id}': f"{parameter['name']} - Campo {parameter['required']}"})
                        items_text(pdf, spec, f'parameter{id}', f"{parameter['name']} - Campo {parameter['required']}")
                    else:
                        testes.update({f'parameter{id}': f"{parameter['name']}"})
                        items_text(pdf, spec, f'parameter{id}', f"{parameter['name']}")
                    for status, status_object in verb_object['responses'].items():
                        id = id + 1
                        testes.update({f'status{id}': status})
                        items_text(pdf, spec, f'status{id}', status)
                        count = 0
                        for schema, schema_objets in status_object.items():
                            if count == 0:
                                count = count + 1
                                id = id + 1
                                testes.update({f'schema{id}': schema})
                                items_text(pdf, spec, f'schema{id}', schema)
                            else:
                                continue
    return testes


"""
  Valida o inicio da string, passando por parametro o texto e a variavel
"""


def valida_inicio_string(texto, prefixo):
    return texto.startswith(prefixo)


"""
  Funções para configurar os subtitulos
"""


def subtitle_path(pdf, string):
    try:
        pdf.setFont("Helvetica-Oblique", 14)
        pdf.drawString(30, get_altura(), f'Paths: {string}')
    except TypeError:
        print("Erro na função 'subtitle_path' no GeneratorPDF")


def subtitle_verb(pdf, string):
    try:
        pdf.setFont("Helvetica-Oblique", 13)
        pdf.drawString(50, get_altura(), f'Metódos: {string}')
    except TypeError:
        print("Erro na função 'subtitle_verb' no GeneratorPDF")


def subtitle_cmp(pdf, string):
    try:
        pdf.setFont("Helvetica-Oblique", 11)
        pdf.drawString(80, get_altura(), f'Parametros: {string}')
    except TypeError:
        print("Erro na função 'subtitle_cmp' no GeneratorPDF")


def subtitle_status(pdf, string):
    try:
        pdf.setFont("Helvetica-Oblique", 10)
        pdf.drawString(100, get_altura(), f'Status Code: {string}')
    except TypeError:
        print("Erro na função 'subtitle_status' no GeneratorPDF")


def subtitle_schema(pdf, string):
    try:
        palavra = string
        pdf.setFont("Helvetica-Oblique", 9)
        pdf.drawString(150, get_altura(), f'Schemas: {palavra}')
    except TypeError:
        print("Erro na função 'subtitle_schema' no GeneratorPDF")


def subtitle(pdf, string):
    try:
        pdf.setFont("Helvetica-Oblique", 8)
        pdf.drawString(150, get_altura(), f'Outros: {string}')
    except TypeError:
        print("Erro na função 'subtitle' no GeneratorPDF")


"""
  Determina qual o subtitulo conforme o dado que está sendo passado por parametro
"""


def subtitle_items(pdf, string, value, spec):
    set_altura(new_page(pdf, 10, spec))
    if valida_inicio_string(string, "path"):
        subtitle_path(pdf, string)
    elif valida_inicio_string(string, "verb"):
        subtitle_verb(pdf, value)
    elif valida_inicio_string(string, "parameter"):
        subtitle_cmp(pdf, value)
    elif valida_inicio_string(string, "status"):
        subtitle_status(pdf, value)
    elif valida_inicio_string(string, "schema"):
        subtitle_schema(pdf, value)
    else:
        subtitle(pdf, value)


'''
  Gera novas páginas quando o contéudo chega no final
'''


def new_page(pdf, num, spec):
    try:
        if get_altura() <= 80:
            pdf.showPage()
            set_altura(700)

            # Logo
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawImage("setup/static/img/logo.png", 15, 755, width=160, height=80)

            # Titulo: Plano de Testes de API
            title_header(pdf, spec)

            return get_altura()
        else:
            set_altura(get_altura() - num)
            return get_altura()
    except AttributeError:
        print(f"Erro ao gerar nova página")
        return 0


"""
  Title: TESTES
"""


def title_Testes(pdf):
    set_altura(get_altura() - 50)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, get_altura(), "Testes")
    pdf.setLineWidth(1)
    pdf.line(30, get_altura() - 30, 550, get_altura() - 30)
    set_altura(get_altura() + 30)


"""
  Casos de Testes
"""


def subtitle_path(pdf, string):
    pdf.setFont("Helvetica-Oblique", 12)
    pdf.drawString(30, get_altura(), string)


def imprime_item(pdf, id, descricao, item):
    set_altura(get_altura() - 15)
    subtitle_path(pdf, f'Caso de Testes {id}')
    set_altura(get_altura() - 15)
    subtitle_path(pdf, f'{separa_string_poste(descricao)} : {item}')
    set_altura(get_altura() - 10)


def imprime_observacao(pdf, item):
    set_altura(get_altura() - 15)
    subtitle_path(pdf, f'Observação:  {item}')
    set_altura(get_altura() - 10)


def montando_testes(pdf, ordem, spec):
    set_altura(get_altura() - 55)
    testes = {}
    id = 0
    for descricao, path in ordem.items():
        id = id + 1
        new_page(pdf, 15, spec)
        print(descricao)
        if valida_inicio_string(separa_string_poste(descricao), "Requesicao"):
            imprime_item(pdf, id, descricao, path)
        elif valida_inicio_string(separa_string_poste(descricao), "verbo"):
            imprime_item(pdf, id, descricao, path)
        elif valida_inicio_string(separa_string_poste(descricao), "Parameter"):
            imprime_item(pdf, id, descricao, path)
        elif valida_inicio_string(separa_string_poste(descricao), "status"):
            imprime_item(pdf, id, descricao, path)
        elif valida_inicio_string(separa_string_poste(descricao), "schema"):
            imprime_item(pdf, id, descricao, path)
        elif valida_inicio_string(descricao, "oservacao"):
            imprime_observacao(pdf, path)
        else:
            #print(get_altura())
            continue


def separa_string_poste(string):
    texto = string
    dado = texto.split('-')[0].strip()
    return dado

