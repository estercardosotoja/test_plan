from django.urls import path, include
from app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('manual/', manual, name='manual'),
    path('contato/', contato, name='contato'),
    path('gerador/', gerador, name='gerador'),
    path('download/', download, name='download'),
]