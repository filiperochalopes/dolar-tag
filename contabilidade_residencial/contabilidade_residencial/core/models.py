from django.db import models
import datetime

# Create your models here.


class Pessoa(models.Model):
    nome = models.CharField("Nome", max_length=100)
    email = models.EmailField(blank=True, unique=True)


class PropriedadePessoa(models.Model):
    chave = models.CharField("Chave", max_length=100)
    valor = models.CharField("Valor", max_length=200)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)


class Banco(models.Model):
    codigo = models.CharField(max_length=5, blank=True)
    nome = models.CharField(max_length=100, blank=True)
    agencia = models.CharField(max_length=20, blank=True)
    conta = models.CharField(max_length=20, blank=True)
    apelido = models.CharField(max_length=100, unique=True)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Tag(models.Model):
    nome = models.TextField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)  # Pode ser vazio
    cor_hex = models.TextField(max_length=6)
    # https://stackoverflow.com/questions/4246000/how-to-call-python-functions-dynamically RESPOSTA 2
    funcao = models.TextField(max_length=6, blank=True)
    pai = models.ForeignKey('Tag', on_delete=models.CASCADE, blank=True, null=True)


class Registro(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    valor = models.FloatField()
    descricao = models.TextField(blank=True)  # Pode ser vazio
    tags = models.ManyToManyField(Tag)
    data = models.DateField(blank=False, default=datetime.date.today)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
