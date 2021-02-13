import json
from time import time

from django.urls import reverse_lazy
from django.views.generic import View,ListView,UpdateView,CreateView,DeleteView,TemplateView
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db import connection
from django.http import JsonResponse

#Clases Heredadas de proyecto
from apps.proyecto.views import _FormValid, _FormValidFiltros,	\
		_CrearFormValid, _EliminarPermanentemente, _EliminarCambiandoEstado, \
		_ValidarInputAjax, _SearchNombreAjax


from .models import Actor,Reglas
from .forms import ActorForm
from .filters import ActorFilter

#-----------------------------------------------------------------------------------------------
#Actor
#-----------------------------------------------------------------------------------------------

class ListarActor(_FormValidFiltros):
	model = Actor
	permission_required = 'stakeholders.viewractor'
	template_name = 'stakeholders/actor/listar_actor.html'
	filter_class = ActorFilter
	form_class = ActorForm

	def get_queryset(self):
		qs = self.model.objects.all().select_related('organizacion_id')
		product_filtered_list = self.filter_class(self.request.GET, queryset=qs)
		return product_filtered_list.qs,product_filtered_list #Django Filter (https://riptutorial.com/es/django/example/21255/utilice-django-filter-con-cbv)

class CrearActor(_CrearFormValid):
	model = Actor
	permission_required = 'stakeholders.add_actor'
	form_class = ActorForm
	template_name = 'stakeholders/actor/crear_actor.html'
	success_url = reverse_lazy('stakeholders:ListarActor')
	success_message = 'El Actor fue creado con éxito'
	error_message = 'No se guardo con exito.'
	
class EditarActor(_FormValid,UpdateView):
	model = Actor
	permission_required = 'stakeholders.change_actor'
	form_class = ActorForm
	template_name = 'stakeholders/actor/editar_actor.html'
	success_url = reverse_lazy('stakeholders:ListarActor')
	success_message = 'El Actor fue editado con éxito'
	error_message = 'No se guardo con exito.'

class EliminarActor(_EliminarPermanentemente):
	model = Actor
	permission_required = 'stakeholders.delete_actor'
	template_name = 'stakeholders/actor/actor_confirm_delete.html'
	success_message = 'El actor fue eliminado con éxito'
	error_message = 'No se guardo con exito.'
	success_url = reverse_lazy('stakeholders:ListarActor')

class EliminarActorEstado(_FormValid,DeleteView):
	model = Actor
	permission_required = 'stakeholders.delete_actor'
	template_name = 'stakeholders/actor/actor_confirm_delete.html'
	success_url = reverse_lazy('stakeholders:ListarActor')
	success_message = 'El actor fue eliminado con éxito'
	error_message = 'No se guardo con exito.'

	def get(self, request, *args, **kwargs):
		obj = get_object_or_404(self.model, pk = kwargs['id'])
		print("obj.estado --> ",obj.estado)
		if obj.estado:
			obj.eliminado = True
			obj.save()
			messages.success(self.request, self.success_message, extra_tags='God Job')
		elif obj.estado == False:
			messages.info(self.request, 'Ya se encuentra desactivado')
		else:
			messages.error(self.request, self.error_message, extra_tags='Error')

class ValidarInputActor(_ValidarInputAjax):
	model = Actor
	permission_required = 'stakeholders.add_actor'

class SearchActorAjax(_SearchNombreAjax):
	model = Actor
	permission_required = 'stakeholders.add_actor'