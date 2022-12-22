# TestPlan
Uma ferramenta geradora de testes funcionais para API.

## Objetivos:

Projeto Tecnologico de conclusão de curso.

## Tecnologias:

### Linguagens:

- Python
- CSS
- HTML

### Framework:

#### - Django: 

Framework utilizado para realizar o desenvolvimento da aplicação web.

#### - Bootstrap: 

Framework que auxilia com o estilo e templates prontos de html e css.

### Banco de Dados:

#### - Postgree

### Bibliotecas:

- asgiref
- Django 
- python-dotenv 
- sqlparse
- tzdata
- Pillow 
- psycopg2
- psycopg2-binary
- pytz
- PyYAML
- somewhere


## Comando para executar:
- **1** - Criar um ambiente virtual para isolar as importações necessárias:

       python -m venv nome_ambiente_virtual

- **2** - Ativar o ambiente virtual:

! Nesta etapa depende de qual o sistema operacional, para Windowns:

    nome_ambiente_virtual\Scripts\activate.bat

- **3** - Agora, podemos instalar todas as importações necessárias para executar o código:

! As importações estão listadas no arquivo requirements.txt

      pip install -r requirements.txt

- **4** - Para iniciar um servidor para acessar a aplicação execute este comando:

      python manage.py runserver

- **5** - Depois de utilizar a aplicação pode desativar do ambiente virtual pelo comando:

      deactivate