# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

from apps.stakeholders.models import Actor

class Metodologia(models.Model):
	nombre = models.CharField('Nombre',max_length=50,blank=False,null=False, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Metodologia"
		verbose_name_plural = "Metodologias"

class Tag(models.Model):
	nombre = models.CharField('Nombre', max_length=150, blank=True,null=True,unique=True)
	history = HistoricalRecords()

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Tag"
		verbose_name_plural = "Tags"
		

class Proyecto(models.Model):
	
	nombre = models.CharField('Nombre',max_length=50,blank=False,null=False, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	meta = models.IntegerField('Meta',default=0, blank=False,null=False)
	estado = models.BooleanField(default=True, null=False)
	descripcion = models.TextField('Descripción',max_length=600,blank=True,null=True)
	tipo_prediccion = models.BooleanField(verbose_name=u'tipo de prediccion', default=False)
	link_powerbi = models.CharField('Link PowerBI',max_length=250,blank=True,null=True)

	#relaciones ManyToManyField
	director = models.ManyToManyField(User, related_name='director_proyecto', blank=True,verbose_name=u'Directores')
	colaborador = models.ManyToManyField(User,verbose_name='Colaboradores',related_name='colaborador_proyecto',blank=True)
	metodologia = models.ManyToManyField(Metodologia,related_name='metodologia')
	tags = models.ManyToManyField(Tag, blank=True,related_name='Tag_Proyecto')

	history = HistoricalRecords()

	def __str__(self):
		return str(self.nombre)

	class Meta:
		verbose_name = "Proyecto"
		verbose_name_plural = "Proyectos"


"""
https://dev.to/zachtylr21/model-inheritance-in-django-m0j
Revisar la herencia para performance
"""