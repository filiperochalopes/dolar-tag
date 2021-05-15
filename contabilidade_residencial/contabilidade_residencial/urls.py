"""contabilidade_residencial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from contabilidade_residencial.core import views

urlpatterns = [
    path('', views.registros),
    path('adicionar-registro', views.adicionar_registro),
    path('editar-registro', views.editar_registro),
    path('pessoas', views.pessoas),
    path('adicionar-pessoa', views.adicionar_pessoa),
    path('editar-pessoa', views.editar_pessoa),
    path('bancos', views.bancos),
    path('adicionar-banco', views.adicionar_banco),
    path('editar-banco', views.editar_banco),
    path('tags', views.tags),
    path('recorrente', views.recorrente),
    path('admin/', admin.site.urls),
    path('api/banco', views.rest_banco),
    path('api/registro/<int:id>', views.rest_registro),
]
