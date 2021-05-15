from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from .models import Pessoa, PropriedadePessoa, Banco, Registro, Tag
from django.views.decorators.csrf import csrf_exempt
from functools import reduce
from datetime import datetime
import re


def registros(request):
    registros = Registro.objects
    pessoas = Pessoa.objects.all()

    # Elementos de filtragem
    pesquisa = request.GET.get('q') or ""
    debito = bool(request.GET.get('debito')) or True
    credito = bool(request.GET.get('credito')) or True
    bancos = request.GET.getlist('banco[]') or None

    dates = re.findall("\d{1,2}\/\d{1,2}\/\d{2,4}", pesquisa)
    if(len(dates) == 2):
        registros = registros.filter(data__range=[datetime.strptime(
            dates[0], '%d/%m/%Y').strftime('%Y-%m-%d'), datetime.strptime(
            dates[1], '%d/%m/%Y').strftime('%Y-%m-%d')])
    elif(len(dates) == 1):
        registros = registros.filter(data=datetime.strptime(
            dates[0], '%d/%m/%Y').strftime('%Y-%m-%d'))

    pesquisa = re.sub("\d{1,2}\/\d{1,2}\/\d{2,4}", "", pesquisa)

    busca_like = re.search("\".+\"", pesquisa)
    if(busca_like):
        busca_like = re.sub("\"", "", busca_like[0])
        registros = registros.filter(descricao__icontains=busca_like)

    pesquisa = re.sub("\".+\"", "", pesquisa)

    if(bancos):
        registros = registros.filter(banco_id__in=bancos)

    if(credito and not debito):
        registros = registros.filter(valor__gt=0)

    if(debito and not credito):
        registros = registros.filter(valor__lt=0)

    tags = re.findall("\w+", pesquisa)

    if(len(tags)):
        registros = registros.filter(tags__nome__in=tags)

    # Mostrando todos os registros filtrados em ordem de data
    registros = registros.order_by('-data').all()

    # Calculando os valores totais de balanço
    creditos = reduce(lambda accumulated,current: accumulated+current.valor if current.valor > 0 else accumulated, registros, 0)
    debitos = reduce(lambda accumulated,current: accumulated+current.valor if current.valor < 0 else accumulated, registros, 0)
    balanco = reduce(lambda accumulated,current: accumulated+current.valor, registros, 0)

    for pessoa in pessoas:
        bancos = Banco.objects.filter(pessoa=pessoa)
        pessoa.bancos = bancos

    return render(request, 'registros.html', {
        'registros': registros, 
        'pessoas': pessoas,
        'analise': {
            'creditos': creditos,
            'debitos': debitos,
            'balanco': balanco
        }
        })

def recorrente(request):
    registros_recorrentes = Registro.objects.filter(tags__nome='recorrente').all()
    return render(request, 'recorrente.html', {'registros_recorrentes': registros_recorrentes})


def adicionar_registro(request):
    mensagem = None
    cor = None
    pessoas = Pessoa.objects.all()
    if request.method == 'POST':
        try:
            registro = Registro()
            pessoa = Pessoa.objects.get(id=request.POST.get('pessoa_id'))
            banco = Banco.objects.get(id=request.POST.get('banco_id'))
            registro.pessoa = pessoa
            registro.banco = banco
            registro.data = request.POST.get('data')
            registro.valor = request.POST.get('valor')
            registro.descricao = request.POST.get('descricao')
            tags = request.POST.getlist('tags[]')
            registro.save()

            for tag in tags:
                if tag is not None and tag != '':
                    try:
                        novaTag = Tag()
                        novaTag.nome = tag
                        novaTag.cor_hex = 'cccccc'
                        novaTag.save()
                        registro.tags.add(novaTag)
                    except:
                        try:
                            tagExistente = Tag.objects.get(nome=tag)
                            registro.tags.add(tagExistente)
                        except Exception as e:
                            raise(e)
                            mensagem = f"Erro ao adicionar: {e}"
                            cor = "#e52222"

            mensagem = "Adicionado com sucesso!"
            cor = "#7ee534"
        except Exception as e:
            mensagem = f"Erro ao adicionar: {e}"
            cor = "#e52222"

    return render(request, 'adicionar_registro.html', {'mensagem': mensagem, 'cor': cor, 'pessoas': pessoas})


def editar_registro(request):
    mensagem = None
    cor = None
    pessoas = Pessoa.objects.all()
    registro = Registro.objects.get(id=request.GET.get('id'))
    bancos = Banco.objects.filter(pessoa=registro.pessoa).all()
    if request.method == 'POST':
        try:
            pessoa = Pessoa.objects.get(id=request.POST.get('pessoa_id'))
            banco = Banco.objects.get(id=request.POST.get('banco_id'))
            registro.pessoa = pessoa
            registro.banco = banco
            registro.data = request.POST.get('data')
            registro.valor = request.POST.get('valor')
            registro.descricao = request.POST.get('descricao')
            tags = request.POST.getlist('tags[]')
            registro.save()

            for tag in registro.tags.all():
                if tag not in tags:
                    registro.tags.remove(tag)

            for tag in tags:
                if tag is not None and tag != '':
                    try:
                        novaTag = Tag()
                        novaTag.nome = tag
                        novaTag.cor_hex = 'cccccc'
                        novaTag.save()
                        registro.tags.add(novaTag)
                    except:
                        try:
                            tagExistente = Tag.objects.get(nome=tag)
                            registro.tags.add(tagExistente)
                        except Exception as e:
                            mensagem = f"Erro ao atualizar tags: {e}"
                            cor = "#e52222"

            mensagem = "Atualizado com sucesso!"
            cor = "#7ee534"
        except Exception as e:
            mensagem = f"Erro ao atualizar: {e}"
            cor = "#e52222"

    return render(request, 'editar_registro.html', {'mensagem': mensagem, 'cor': cor, 'pessoas': pessoas, 'registro': registro, 'bancos': bancos})


def pessoas(request):
    mensagem = None
    cor = None
    if(request.GET.get('delete')):
        delete_id = request.GET.get('delete')
        try:
            pessoa = Pessoa.objects.get(id=delete_id)
            pessoa.delete()
            mensagem = f'{pessoa.nome} excluído(a) com sucesso'
            cor = "#7ee534"
        except Pessoa.DoesNotExist:
            mensagem = f'Pessoa de id {delete_id} não existe'
            cor = '#e52222'
    pessoas = Pessoa.objects.all()
    for pessoa in pessoas:
        propriedades = PropriedadePessoa.objects.filter(pessoa=pessoa)
        pessoa.propriedades = propriedades
        bancos = Banco.objects.filter(pessoa=pessoa)
        pessoa.bancos = bancos
    return render(request, 'pessoas.html', {'pessoas': pessoas, 'mensagem': mensagem, 'cor': cor})


def adicionar_pessoa(request):
    mensagem = None
    cor = None
    if request.method == 'POST':
        pessoa = Pessoa()
        pessoa.nome = request.POST.get('nome')
        pessoa.email = request.POST.get('email')
        pessoa.save()
        propriedades = [[request.POST.getlist('propriedades_chave[]')[i], request.POST.getlist('propriedades_valor[]')[
            i]] for i in range(len(request.POST.getlist('propriedades_chave[]')))]

        for propriedade in propriedades:
            propriedade_pessoa = PropriedadePessoa()
            propriedade_pessoa.chave = propriedade[0]
            propriedade_pessoa.valor = propriedade[1]
            propriedade_pessoa.pessoa = pessoa
            propriedade_pessoa.save()

        mensagem = "Adicionado com sucesso!"
        cor = "#7ee534"

    return render(request, 'adicionar_pessoa.html', {'mensagem': mensagem, 'cor': cor})


def editar_pessoa(request):
    pessoa = Pessoa.objects.get(id=request.GET.get('id'))
    propriedades = PropriedadePessoa.objects.filter(pessoa=pessoa)
    pessoa.propriedades = propriedades

    return render(request, 'editar_pessoa.html', {'pessoa': pessoa})


def bancos(request):
    return render(request, 'bancos.html')


def adicionar_banco(request):
    mensagem = None
    cor = None
    pessoas = Pessoa.objects.all()
    if request.method == 'POST':
        pessoa = Pessoa.objects.get(id=request.POST.get('pessoa_id'))
        banco = Banco()
        banco.pessoa = pessoa
        banco.apelido = request.POST.get('apelido')
        banco.codigo = request.POST.get('codigo')
        banco.nome = request.POST.get('nome')
        banco.agencia = request.POST.get('agencia')
        banco.conta = request.POST.get('conta')
        try:
            banco.save()
            mensagem = "Adicionado com sucesso!"
            cor = "#7ee534"
        except Exception as e:
            mensagem = f"Erro ao adicionar {e}"
            cor = "#e52222"

    return render(request, 'adicionar_banco.html', {'mensagem': mensagem, 'cor': cor, 'pessoas': pessoas})


def editar_banco(request):
    return render(request, 'editar_banco.html')


def tags(request):
    tags = Tag.objects.all()
    return render(request, 'tags.html', {'tags': tags})

def rest_banco(request):
    pessoa = Pessoa.objects.get(id=request.GET.get('pessoa_id'))
    bancos = Banco.objects.filter(pessoa=pessoa)
    serialized_query = serializers.serialize('json', bancos)
    return JsonResponse(serialized_query, safe=False)


def rest_registro(request, id):
    registro = None
    if(request.method == 'DELETE'):
        print(f'Excluindo Registro {id}')
        registro = Registro.objects.filter(id=30)
        serialized_query = serializers.serialize('json', registro)
        registro.delete()
    return JsonResponse(serialized_query, safe=False)
