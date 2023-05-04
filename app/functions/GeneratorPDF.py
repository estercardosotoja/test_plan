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

    def Gerar(spec):
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

        # Titulo/Nome do serviço
        pdf.save()
        print('{}.pdf criado com sucesso!'.format(name_pdf))
        return 1


def set_altura(value):
    global altura
    altura = value


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
    sub_titulo = spec['spec']['info']['title']
    pdf.setFont("Helvetica-Oblique", 16)
    pdf.drawString(225, 740, sub_titulo)


"""
  Descrição da aplicação:
"""


def description_header(pdf, spec):
    description = spec['spec']['info']['description']
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(30, 720, f'Description: {description}')


"""
  Version:
"""


def version_header(pdf, spec):
    version = spec['spec']['info']['version']
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(30, 700, f'Version: {version}')


"""
  Host:
"""


def host_header(pdf, spec):
    host = spec['spec']['host']
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(200, 700, f'Host: {host}')


"""
  Base:
"""


def base_header(pdf, spec):
    base = spec['spec']['basePath']
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(450, 700, f'basePath: {base}')


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
    subtitle_items(pdf, item, value, get_altura(), spec)


"""
  Monta um dict com todos os itens da specificação para listar os items
"""


def todos_os_items(pdf, spec):
    set_altura(600)
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
                            items_text(pdf, spec, f'parameter{id}', f"{parameter['name']} - {parameter['type']} - Campo {tipo_campo}")
                        else:
                            tipo_campo = "Obrigatório"
                            testes.update(
                                {f'parameter{id}': f"{parameter['name']} - {parameter['type']} - Campo {tipo_campo}"})
                            items_text(pdf, spec, f'parameter{id}', f"{parameter['name']} - {parameter['type']} - Campo {tipo_campo}")
                    elif parameter.get("type") is not None:
                        id = id + 1
                        testes.update({f'parameter{id}': f"{parameter['name']} - {parameter['type']}"})
                        items_text(pdf, spec,  f'parameter{id}', f"{parameter['name']} - {parameter['type']}")
                    elif parameter.get("required") is not None:
                        testes.update({f'parameter{id}': f"{parameter['name']} - Campo {parameter['required']}"})
                        items_text(pdf, spec, f'parameter{id}', f"{parameter['name']} - Campo {parameter['required']}")
                    else:
                        testes.update({f'parameter{id}': f"{parameter['name']}"})
                        items_text(pdf, spec, f'parameter{id}', f"{parameter['name']}")
                    for status, status_object in verb_object['responses'].items():
                        id = id + 1
                        testes.update({f'status{id}': status})
                        for schema, schema_objets in status_object.items():
                            id = id + 1
                            testes.update({f'schema{id}': schema})
                            items_text(pdf, spec, f'schema{id}', schema)
    return testes


"""
  Valida o inicio da string, passando por parametro o texto e a variavel
"""


def valida_inicio_string(texto, prefixo):
    return texto.startswith(prefixo)


"""
  Funções para configurar os subtitulos
"""


def subtitle_path(pdf, string, altura):
    pdf.setFont("Helvetica-Oblique", 14)
    pdf.drawString(30, altura, f'Paths: {string}')


def subtitle_verb(pdf, string, altura):
    pdf.setFont("Helvetica-Oblique", 13)
    pdf.drawString(50, altura, f'Metódos: {string}')


def subtitle_cmp(pdf, string, altura):
    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawString(80, altura, f'Parametros: {string}')


def subtitle_status(pdf, string, altura):
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(100, altura, f'Status Code: {string}')


def subtitle_schema(pdf, string, altura):
    palavra = string
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(150, altura, f'Schemas: {palavra}')


def subtitle(pdf, string, altura):
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawString(150, altura, f'Outros: {string}')


"""
  Determina qual o subtitulo conforme o dado que está sendo passado por parametro
"""


def subtitle_items(pdf, string, value, altura, spec):
    set_altura(new_page(pdf, 10, spec))
    if valida_inicio_string(string, "path"):
        subtitle_path(pdf, value, altura )
    elif valida_inicio_string(string, "verb"):
        subtitle_verb(pdf, value, altura)
    elif valida_inicio_string(string, "parameter"):
        subtitle_cmp(pdf, value, altura)
    elif valida_inicio_string(string, "status"):
        subtitle_status(pdf, value, altura)
    elif valida_inicio_string(string, "schema"):
        subtitle_schema(pdf, value, altura)
    else:
        subtitle(pdf, value, altura)


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

