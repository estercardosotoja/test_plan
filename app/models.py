from django.db import models
from datetime import datetime


class FileForms(models.Model):
    arquivo_especificacao = models.FileField()
    date_create = models.DateTimeField(default=datetime.now, blank=True)
