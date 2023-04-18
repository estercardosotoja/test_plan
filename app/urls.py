from django.urls import path, include
from app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('gerador/', generator, name='gerador'),
    path('confirm/', confirm, name='confirm'),
    path('download/', download, name='download'),
    path('downloaded/', downloaded, name='downloaded'),
    path('manual/', manual, name='manual'),
    path('contato/', contato, name='contato')
]