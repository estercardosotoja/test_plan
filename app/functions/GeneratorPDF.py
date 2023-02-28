from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class FilePDF:

    # 1 Title e Cabeçalho

    '''
        Configura o template do cabeçalho
    '''
    def cabecalho(self, pdf, infos):
        try:
            #Logo
            #pdf.drawImage("../static/img/logo.png", 15, 755, width=160, height=80)
            # A frase: Plano de Testes de API
            pdf.setFont("Helvetica-Bold", 24)
            pdf.drawString(180, 775, 'Plano de Testes de API')
            # Titulo/Nome do serviço
            pdf.setFont("Helvetica-Oblique", 16)
            pdf.drawString(225, 740, infos['title'])
            return 1
        except AttributeError:
            print(f"Erro ao preencher o cabeçalho")
            return 0

# 2 Informaçoes
    '''
        Preenche o campo destinado a informações
    '''
    def pdf_info(self, pdf, infos):
        try:
            # Informações
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(40, 720, "Informações:")
            pdf.setFont("Helvetica", 12)
            pdf.drawString(40, 700, f"Versão : {infos['versao']}")
            pdf.drawString(40, 685, f"URL : {infos['url']}")
            return 1
        except AttributeError:
            print(f"Erro ao preencher as informações")
            return 0

# 3 End points
    '''
        Preenche o campo destinado o nome dos Paths
    '''
    def pdf_path(self, pdf, paths):
        try:
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(30, 640, "Descrição dos testes:")
            pos_y = 615
            for path in paths:
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(40, pos_y, path)
                pos_y -= 20
        except AttributeError:
            print(f"Erro ao preencher as descrição dos testes")
            return 0
# 4 Verbs
    '''
        Preenche o campo destinado os Verbs
    '''
    def pdf_verbs(self, pdf, verbs):
        try:
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(30, 640, "Verbs dos testes:")
            pos_y = 615
            for end, verb in verbs.items():
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(40, pos_y, end)
                pos_y -= 20
                for i in verb:
                    pdf.setFont("Helvetica-Bold", 12)
                    pdf.drawString(50, pos_y, i)
                    pos_y -= 20
                    pos_y = self.new_page(pdf, pos_y)
        except AttributeError:
            print(f"Erro ao preencher os verbos dos testes")
            return 0

    '''
       Gera novas páginas quando o contéudo chega no final
    '''
    def new_page(self, pdf, pos_y):
        try:
            if pos_y <= 15:
                pdf.showPage()
                pos_y = 700
                return pos_y
            else:
                return pos_y
        except AttributeError:
            print(f"Erro ao gerar nova página")
            return 0
# 5 Rodape
# Salvar

    def GeneratePDF(self, infos, paths, verbs):
        nome_pdf = 'testplan'
        pdf = canvas.Canvas('{}.pdf'.format(nome_pdf), pagesize=A4)
        self.cabecalho(pdf, infos)
        #Info
        self.pdf_info(pdf, infos)
        # Testes
        self.pdf_verbs(pdf, verbs)
        pdf.save()
        print('{}.pdf criado com sucesso!'.format(nome_pdf))


"""
a = Extrator(PATH_JSON)
infos = a.info()
paths = a.path()
verbs = a.verbs_new()
a.generatePDF(infos, paths, verbs)
"""