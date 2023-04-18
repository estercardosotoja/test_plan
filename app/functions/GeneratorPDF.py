from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import Paragraph


class GeneratorPDF:
    """
        Gera o PDF
    """

    def Gerar(dados):
        altura = 700
        # Intanciar arquivo
        name_pdf = "testplan"
        diretorio = "media/testplan/"
        caminho_completo = diretorio + name_pdf
        pdf = canvas.Canvas('{}.pdf'.format(caminho_completo), pagesize=A4)
        for key, value in dados.items():
            altura = altura - 30
            element_type(value, key, pdf, altura)
        # Logo
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawImage("setup/static/img/logo.png", 15, 755, width=160, height=80)
        # A frase: Plano de Testes de API
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawString(180, 775, 'Plano de Testes de API')
        # Titulo/Nome do serviço
        pdf.setFont("Helvetica-Oblique", 16)
        pdf.drawString(225, 740, "TESTES DE API")
        pdf.save()
        print('{}.pdf criado com sucesso!'.format(name_pdf))
        return 1


"""
    Determina a cor dos verbos
"""


def element_type(value, key, pdf, altura):
    if value == "path":
        font_path(pdf)
        pdf.drawString(100, altura, 'EndPoint:     ' + key)
    elif value == 'verb':
        font_verb(pdf)
        if key == 'post':
            # green
            pdf.setFillColorRGB(153, 4, 50)
            pdf.drawString(150, altura, key.upper())
        elif key == 'get':
            # blue
            pdf.setFillColorRGB(0, 127, 255)
            pdf.drawString(150, altura, key.upper())
            return altura
        elif key == 'delete':
            # red
            pdf.setFillColorRGB(255, 0, 0)
            pdf.drawString(150, altura, key.upper())
            return altura
        elif key == 'put':
            # orange
            pdf.setFillColorRGB(205, 127, 50)
            pdf.drawString(150, altura, key.upper())
            return altura
        elif key == 'PATCH':
            # blue clean
            pdf.setFillColorRGB(0, 255, 255)
            pdf.drawString(150, altura, key.upper())
            return altura
        else:
            # gray
            pdf.setFillColorRGB(168, 168, 168)
            pdf.drawString(150, altura, key.upper())
            return altura
    else:
        font_verb(pdf)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(200, altura, key)


"""
    Determina a fonte do path
"""

def font_path(pdf):
    pdf.setFont("Helvetica-Bold", 12)


"""
    Determina a fonte dos verbs
"""
def font_verb(pdf):
    pdf.setFont("Helvetica-Bold", 10)
