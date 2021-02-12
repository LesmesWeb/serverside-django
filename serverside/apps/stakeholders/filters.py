import django_filters
from django_filters import DateFilter, CharFilter
from .models import Actor,Reglas
from distutils.util import strtobool

from apps.proyecto.filters import _BaseFilter


class ActorFilter(_BaseFilter):
	class Meta:
		model = Actor
		fields=['nombre','start_date','end_date','genero']

class ReglasFilter(_BaseFilter):

	class Meta:
		model = Reglas
		fields=['nombre','start_date','end_date']
