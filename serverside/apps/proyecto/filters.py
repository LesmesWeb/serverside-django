import django_filters
from django_filters import DateFilter, CharFilter
from .models import Proyecto,Metodologia
from django import forms
from django.forms import ModelForm
from distutils.util import strtobool

class _BaseFilter(django_filters.FilterSet):

	nombre = CharFilter(field_name="nombre",lookup_expr='icontains')
	start_date = DateFilter(field_name="created_at",lookup_expr='gte')
	end_date = DateFilter(field_name="created_at",lookup_expr='lte')

	class Cliente:
		model = Metodologia
		fields=['nombre','start_date','end_date']

class ProyectoFilter(_BaseFilter):

	TRUE_FALSE_CHOICES = (
		('', 'Estados Categorizados'),
		(True, 'Activo'),
		(False, 'Inactivo')
	)

	estado = django_filters.TypedChoiceFilter(choices=TRUE_FALSE_CHOICES,
                                            coerce=strtobool)

	class Meta:
		model = Proyecto
		#fields = '__all__' #para traer todos los campos
		#exclude = ['proyecto','finished']
		fields=['start_date','end_date','nombre','estado']

class MetodologiaFilter(_BaseFilter):

	class Cliente:
		model = Metodologia
		fields=['nombre','start_date','end_date']