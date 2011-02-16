from django.db import models
import datetime

class Artigo(models.Model):
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    publicacao = models.DateTimeField()
	
    def __unicode__(self):
        return '[' + self.titulo + '] - ' + self.conteudo[0:50] + '...'


class Pessoa(models.Model):
    nome = models.CharField(max_length=128)

    def __unicode__(self):
        return self.nome