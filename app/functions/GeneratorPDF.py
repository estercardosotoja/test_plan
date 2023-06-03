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

    def Gerar(spec, context, quant_itens_selecionados):
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
        quantidade_testes = montando_testes(pdf, context, spec)

        # Title Resumo
        title_Resumo(pdf, spec)

        # Dados
        resumo(pdf, quant_itens_selecionados, quantidade_testes, spec)

        # Titulo/Nome do serviço
        pdf.save()
        print('Log: {}.pdf criado com sucesso!'.format(name_pdf))
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
        print("Log: Erro na função 'title_header' no GeneratorPDF")


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
        print("Log: Erro na função 'sub_title_header' no GeneratorPDF")


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
            return
    except TypeError:
        print("Log: Erro na função 'description_header' no GeneratorPDF")


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
            return
    except KeyError:
        print("Log: Erro na função 'host_header' no GeneratorPDF")


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
            return
    except KeyError:
        print("Log: Erro na função 'host_header' no GeneratorPDF")


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
            return
    except KeyError:
        print("Log: Erro na função 'host_header' no GeneratorPDF")


"""
  Title: ITEMS
"""


def title_items(pdf):
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, 670, "Elementos que contém na especificação")
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
                    id = id + 1
                    if parameter is None:
                        id = id - 1
                        print(f"testes vszio: {parameter}")
                    elif parameter.get("name") is None:
                        id = id - 1
                        print(f"testes vazio: {parameter}")
                    elif parameter.get("type") is not None and parameter.get('required') is not None:
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
                                id = id + 1
                                count = count + 1
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
        set_altura(get_altura() - 10)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(30, get_altura(), f' Endpoint: {string}')
    except TypeError:
        print("Log: Erro na função 'subtitle_path' no GeneratorPDF")


def subtitle_verb(pdf, string):
    try:
        pdf.setFont("Helvetica-Oblique", 14)
        pdf.drawString(40, get_altura(), f' Metódos: {string.upper()}')
    except TypeError:
        print("Log: Erro na função 'subtitle_verb' no GeneratorPDF")


def subtitle_cmp(pdf, string):
    try:
        pdf.setFont("Helvetica-Oblique", 13)
        pdf.drawString(50, get_altura(), f' Campos: {string}')
    except TypeError:
        print("Log: Erro na função 'subtitle_cmp' no GeneratorPDF")


def subtitle_status(pdf, string):
    try:
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(60, get_altura(), f'Status Code: {string}')
    except TypeError:
        print("Log: Erro na função 'subtitle_status' no GeneratorPDF")


def subtitle_schema(pdf, string):
    try:
        palavra = string
        pdf.setFont("Helvetica-Oblique", 11)
        pdf.drawString(70, get_altura(), f'Schemas: {palavra}')
    except TypeError:
        print("Log: Erro na função 'subtitle_schema' no GeneratorPDF")


def subtitle(pdf, string):
    try:
        pdf.setFont("Helvetica-Oblique", 10)
        pdf.drawString(70, get_altura(), f'Outros: {string}')
    except TypeError:
        print("Log: Erro na função 'subtitle' no GeneratorPDF")


"""
  Determina qual o subtitulo conforme o dado que está sendo passado por parametro
"""


def subtitle_items(pdf, string, value, spec):
    set_altura(new_page(pdf, 10, spec))
    if valida_inicio_string(string, "path"):
        subtitle_path(pdf, value)
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
        print(f"Log: Erro ao gerar nova página")
        return 0


"""
  Title: TESTES
"""


def title_Testes(pdf):
    set_altura(get_altura() - 50)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, get_altura(), "Validações")
    pdf.setLineWidth(1)
    pdf.line(30, get_altura() - 30, 550, get_altura() - 30)
    set_altura(get_altura() + 30)


"""
  Casos de Testes
"""


def subtitle_elementos(pdf, string):
    pdf.setFont("Helvetica-Oblique", 12)
    pdf.drawString(30, get_altura(), string)


def acentua_validacao_path(descricao):
    if valida_inicio_string(descricao, 'Requesicao correto'):
        descricao = 'Requisição correta'
    elif valida_inicio_string(descricao, 'Requesicao invalido'):
        descricao = 'Requisição inválida'
    else:
        descricao = 'ERROR'
    return descricao


def acentua_validacao_verb(descricao):
    if valida_inicio_string(descricao, 'Metodo'):
        descricao = 'Método'
    else:
        descricao = 'ERROR'
    return descricao


def acentua_validacao_parameter(descricao):
    if valida_inicio_string(descricao, 'Parametro correto'):
        descricao = 'Campo correto'
    elif valida_inicio_string(descricao, 'Parametro vazio'):
        descricao = 'Campo vazio'
    elif valida_inicio_string(descricao, 'Parametro ausente'):
        descricao = 'Campo ausente'
    elif valida_inicio_string(descricao, 'Parametro com tipo diferente'):
        descricao = 'Campo com tipo de dado diferente'
    else:
        descricao = 'ERROR'
    return descricao


def imprime_item(pdf, id, descricao, item):
    set_altura(get_altura() - 15)
    subtitle_elementos(pdf, f'Caso de Testes {id}')
    set_altura(get_altura() - 15)
    subtitle_elementos(pdf, f'{separa_string_poste(descricao)} : {item}')
    set_altura(get_altura() - 10)


def imprime_observacao(pdf, item):
    set_altura(get_altura() - 15)
    subtitle_path(pdf, f'Observação:  {item}')
    set_altura(get_altura() - 10)


def montando_testes(pdf, ordem, spec):
    set_altura(get_altura() - 55)
    testes = {}
    ident = 0
    for descricao, path in ordem.items():
        ident = ident + 1
        new_page(pdf, 15, spec)
        if valida_inicio_string(separa_string_poste(descricao), "Requesicao"):
            descricao = acentua_validacao_path(descricao)
            imprime_item(pdf, ident, descricao, path)
        elif valida_inicio_string(separa_string_poste(descricao), "Metodo"):
            descricao = acentua_validacao_verb(descricao)
            imprime_item(pdf, ident, descricao, path.upper())
        elif valida_inicio_string(separa_string_poste(descricao), "Parametro"):
            descricao = acentua_validacao_parameter(descricao)
            imprime_item(pdf, ident, descricao, path)
        elif valida_inicio_string(separa_string_poste(descricao), "Status"):
            imprime_item(pdf, ident, descricao, path)
        elif valida_inicio_string(separa_string_poste(descricao), "Schema"):
            imprime_item(pdf, ident, descricao, path)
        elif valida_inicio_string(descricao, "observacao"):
            ident = ident - 1
            imprime_observacao(pdf, path)
        else:
            continue
    return ident


def separa_string_poste(string):
    texto = string
    dado = texto.split('-')[0].strip()
    return dado


# Title Resumo
def title_Resumo(pdf, spec):
    set_altura(get_altura() - 50)
    new_page(pdf, 10, spec)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, get_altura(), "Métricas")
    pdf.setLineWidth(1)
    pdf.line(30, get_altura() - 30, 550, get_altura() - 30)
    set_altura(get_altura() + 30)


# Dados
def resumo(pdf, quantidade_itens_selecionados, quantidade_testes, spec):
    set_altura(get_altura() - 100)
    new_page(pdf, 10, spec)
    quant_total_itens_specificacao = quantidade_itens_total_specficacao(spec)
    porc_cobertura = porcentagem_cobertura(quant_total_itens_specificacao, quantidade_itens_selecionados)
    text_porc_cobertura = f'{porc_cobertura}%'
    subtitle_quantidade_itens(pdf, 70, f'Itens Totais', quant_total_itens_specificacao)
    subtitle_quantidade_itens(pdf, 165, f'Itens selecionados', quantidade_itens_selecionados)
    subtitle_quantidade_itens(pdf, 280, f'Total de Testes Funcionais', quantidade_testes)
    subtitle_quantidade_itens(pdf, 420, 'Cobertura de Testes', text_porc_cobertura)
    set_altura(get_altura() - 20)


def porcentagem_cobertura(total, selecionados):
    cobertura = ((selecionados * 100) / total)
    porcentagem_arredondada = round(cobertura)
    return porcentagem_arredondada


def subtitle_quantidade_itens(pdf, x, string, num):
    try:
        pdf.setFont("Helvetica-Oblique", 35)
        pdf.drawString(x, get_altura(), f'{num}')
        pdf.setFont("Helvetica-Oblique", 10)
        pdf.drawString(x, get_altura() - 15, f'{string}')
    except TypeError:
        print("Log: Erro na função 'subtitle_path' no GeneratorPDF")


def quantidade_itens_total_specficacao(spec):
    paths = spec["spec"]["paths"]
    count = 0
    for path, objetc_verb in paths.items():
        count = count + 1
        print(f'{count}: {path}')
        for verb, objetc_parameters in objetc_verb.items():
            count = count + 1
            print(f'{count}: {verb}')
            for parameter in objetc_parameters['parameters']:
                count = count + 1
                print(f' Parameter: {count}: {parameter.values()}')
                if parameter is None:
                    count = count - 1
                elif parameter.get("name") is None:
                    count = count - 1
                else:
                    continue
            for status, status_object in objetc_parameters['responses'].items():
                count = count + 1
                print(f'{count}: {status}')
                for schema, schema_objets in status_object.items():
                    if schema == "schema":
                        count = count + 1
                        print(f'{count}: {schema}')
    return count