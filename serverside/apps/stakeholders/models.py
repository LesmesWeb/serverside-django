# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

class Actor(models.Model):
	SEXO = [
		('M', 'Masculino'), 
		('F', 'Femenino'),
	]
	nombre = models.CharField(max_length=200, blank=False,null=False)
	genero = models.CharField('Genero', max_length=2, choices=SEXO, blank=True,null=True)
	alias  = models.CharField('Alias', max_length=200, blank=True,null=True)
	es_autor = models.BooleanField('Es Autor', default=False)
	email = models.CharField(max_length=255, blank=True, null=True)
	es_medio = models.BooleanField('Es Medio', default=False)
	es_persona =models.BooleanField('Es Persona', default=False)
	es_organizacion =  models.BooleanField('Es Organizacion', default=False)
	organizacion_id =models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,verbose_name='Organizacion')
	autorizado = models.BooleanField('autorizado', default=False)
	history = HistoricalRecords()

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Actor"
		verbose_name_plural = "Actores"

class Reglas(models.Model):
	"""
	Representa un nombre alternativo para un medio, se usa para las cargas automaticas
	"""
	actor = models.ForeignKey(Actor, on_delete=models.CASCADE,verbose_name='Reglas Ingestion',blank=False,null=False) #OBLIGATORIO blank=False
	nombre = models.CharField('Nombre',max_length=300, db_index=True, unique=True,blank=False,null=False)
	created_at = models.DateTimeField(_("Fecha de creación"),auto_now_add=True)
	updated_at = models.DateTimeField(_("Fecha de actualización"),auto_now=True)
	history = HistoricalRecords()

	def __str__(self):
		return u'Nombre alterno para {0}: {1}'.format(self.actor.nombre, self.nombre)

	class Meta:
		verbose_name = u'Regla'
		verbose_name_plural = u'Reglas'
