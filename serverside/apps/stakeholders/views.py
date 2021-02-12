import json
from time import time
from django.urls import reverse_lazy
from django.views.generic import View,ListView,UpdateView,CreateView,DeleteView,TemplateView
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import connection
from django.http import JsonResponse

#Models
from .models import Actor,Reglas

#Formularios y filtros
from .forms import ActorForm,ReglasFormCrear,ReglasFormEditar
from .filters import ActorFilter, ReglasFilter

#Clases Heredadas de proyecto
from apps.proyecto.views import _FormValid, _FormValidFiltros,	\
		_CrearFormValid, _EliminarPermanentemente, _EliminarCambiandoEstado, \
		_ValidarInputAjax, _SearchNombreAjax

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

#-----------------------------------------------------------------------------------------------
#Reglas ok (Apoyado de Developer)
#-----------------------------------------------------------------------------------------------

class ListarReglaAjax(PermissionRequiredMixin,ListView):
	model = Reglas
	permission_required = 'stakeholders.view_reglas'
	filter_class = ReglasFilter
	form_class = ReglasFormCrear

	def get_queryset(self):
		#return self.model.objects.select_related('actor').all()
		# n+1 solucionado
		from django.db.models import Q
		#https://books.agiliq.com/projects/django-orm-cookbook/en/latest/or_query.html
		return self.model.objects.select_related('actor').filter(
			Q(nombre__icontains=self.request.GET.get('filtro'))|Q(actor__nombre__icontains=self.request.GET.get('filtro'))
				).values(
					'id',
					'actor__nombre',
					'nombre'
				).order_by(f"{self.request.GET.get('order_by')}")

	def get_context_data(self,**kwargs):
		contexto = {}
		product_filtered_list = self.filter_class(self.request.GET, queryset=self.get_queryset())
		contexto['object_list'] = product_filtered_list.qs  # <QuerySet [{'id': 6, 'actor': 2, 'nombre': 'Nombre regla 2', 'created_at': datetime.datetime(2021, 2, 2, 18, 14, 9, 498719, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 2, 4, 22, 52, 44, 871199, tzinfo=<UTC>)}]>
		contexto['myfilter'] = product_filtered_list 		#<apps.stakeholders.filters.ReglasFilter object at 0x000002474287B988
		contexto['form'] = self.form_class
		return contexto

	def get(self, request, parametro_extra, *args, **kwargs):
		from django.core import serializers
		if request.is_ajax():
			#print("parametro desde URL: ",parametro_extra)
			#print("parametro desde URL kwargs diccionario: ",self.kwargs['parametro_extra'])
			#print("parametro desde URL args tupla: ",self.args)

			"""
				Variable capturadas por GET que ofrece el propio serverSide
			"""

			inicio = int(request.GET.get('inicio'))
			fin = int(request.GET.get('limite'))

			# Variable para inciar el tiempo de ejecución
			tiempo_inicial = time()
			
			data_query = self.get_queryset()
			print("data_query --> ",data_query)
			list_data = []

			"""
			Con el enumerate estoy cargando /stakeholders/reglas/?limite=10&inicio=0&filtro=&order_by=id
			"""
			for indice, valor in enumerate(self.get_queryset()[inicio:inicio+fin],inicio):
				
				valor['num'] = indice+1  #creamos un columna con un indice para mostrar en el datatable
				list_data.append(valor)
			
			tiempo_final = time() - tiempo_inicial

			print(f'Tiempo de ejecución de la consulta: {tiempo_final}')

			data = {
				'length': self.get_queryset().count(),
				'objects': list_data

			}

			return HttpResponse(json.dumps(data),content_type='application/json')
		else:
			# Soliciona el bug de mostrar el Json cuando se da atras
			return redirect('stakeholders:reglas_inicio')

			#return render(request, self.template_name)
			#return self.render_to_response(self.get_context_data()) # error: object has no attribute 'object_list'

class CrearReglaAjax(PermissionRequiredMixin,CreateView):
	model = Reglas
	permission_required = 'stakeholders.add_reglas'
	form_class = ReglasFormCrear
	template_name = 'stakeholders/reglas/crear_regla.html'

	def post(self, request, *args, **kwargs):
				
		print('# of Queries CREAR: {}'.format(len(connection.queries)))

		#Valido el formulario y si cumple que guarde y notifique con SweetAlert el guardado
		if request.is_ajax():
			#cargo los datos del formulario
			form = self.form_class(request.POST)

			#Llamo los datos recibidos en post y los convierto en lista para tenerlos datos del ajax de tags
			form_header = dict(request.POST.lists())
			print("form_header ",form_header['actor'])

			#Valido si contiene información para realizar el filtro
			if  form_header['actor'] == ['']:
				print("Diccionario vacio")
				#capturo los ids de actor (manytomany)
				actor_query = Actor.objects.none()

			else:
				#sino capturo todo los valores
				actor_query = Actor.objects.filter(pk__in=form_header['actor']) 
			print("actor_query ",actor_query)
			
			#print("form.fields['actor'].queryset ",form.fields['actor'].queryset)
			form = self.form_class(request.POST)
			form.fields['actor'].queryset = actor_query
			if form.is_valid():
				print("valido")
				form.save()
				#f'{self.model.__name__} obtienen el nombre del modelo
				mensaje = f'{self.model.__name__} registrado correctamente!'
				error = 'No hay error!'
				response = JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code = 201
				return response

			#De lo contratio que muestre error
			else:
				print("invalido")
				#f'{self.model.__name__} obtienen el nombre del modelo
				mensaje = f'{self.model.__name__} no se ha podido registrar!'
				error = form.errors #DICCIONARIO CON LOS ERRORES
				print("error ",error)
				response = JsonResponse({'mensaje': mensaje, 'error': error})
				response.status_code = 400 #PETICIÓN NO VALIDA POR EL CLIENTE
				return response
		else:
			return redirect('stakeholders:ListarRegla')

class EditarReglaAjax(PermissionRequiredMixin, UpdateView):
	model = Reglas
	permission_required = 'stakeholders.add_reglas'
	form_class = ReglasFormEditar
	template_name = 'stakeholders/reglas/editar_regla.html'

	def get_form(self,*args,**kwargs):

		instance = self.get_object() 
		form = self.form_class(instance=instance)
		print("Verificacion del instance --> ",instance.actor)
		print("Verificacion del actor --> ",form.fields['actor'].queryset)

		#print("Query --> ",form.fields['actor'].queryset)
		#print("instance.actor.all() --> ",instance.actor.all())

		form.fields['actor'].queryset = Actor.objects.all()
		
		from django.db import connection
		print('# of Queries: editar {}'.format(len(connection.queries)))
		#print("get form", form.fields['actor'].queryset)
		#print("instance ---> ",instance) #nombre del campo
		#print("form.fields['tags'] --> ",form.fields['tags'].queryset) #<QuerySet [<Tag: asdsad>, <Tag: prueba 2>]>
		return form

	# Solución al n+1
	def get_queryset(self):
		queryset = self.model.objects.all().select_related('actor')
		return queryset 

	def post(self, request, *args, **kwargs):
				
		from django.db import connection
		from django.http import JsonResponse
		print('# of Queries CREAR: {}'.format(len(connection.queries)))

		#Valido el formulario y si cumple que guarde y notifique con SweetAlert el guardado
		if request.is_ajax():

			#Llamo los datos recibidos en post y los convierto en lista para tenerlos datos del ajax de tags
			form_header = dict(request.POST.lists())
			print("form_header ",form_header['actor'])

			#Valido si contiene información para realizar el filtro
			if  form_header['actor'] == ['']:
				print("Diccionario vacio")
				#capturo los ids de actor (manytomany)
				actor_query = Actor.objects.none()

			else:
				#sino capturo todo los valores
				actor_query = Actor.objects.filter(pk__in=form_header['actor']) 
			print("actor_query ",actor_query)
			
			#print("form.fields['actor'].queryset ",form.fields['actor'].queryset)
			
			#cargo los datos del formulario
			form = self.form_class(request.POST, instance = self.get_object()) #get_object: hace una petición get para obtener el id para no usar una consulta

			form.fields['actor'].queryset = actor_query
			if form.is_valid():
				print("valido")
				form.save()
				#f'{self.model.__name__} obtienen el nombre del modelo
				mensaje = f'{self.model.__name__} Editado correctamente!'
				error = 'No hay error!'
				response = JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code = 201
				print("response")
				return response

			#De lo contratio que muestre error
			else:
				print("invalido")
				#f'{self.model.__name__} obtienen el nombre del modelo
				mensaje = f'{self.model.__name__} no se ha podido Editar!'
				error = form.errors #DICCIONARIO CON LOS ERRORES
				print("error ",error)
				response = JsonResponse({'mensaje': mensaje, 'error': error})
				response.status_code = 400 #PETICIÓN NO VALIDA POR EL CLIENTE
				return response
		else:
			print("ENTRO AL ESLSE")
			return redirect('stakeholders:ListarRegla')

class EliminarReglaAjax(PermissionRequiredMixin, DeleteView):
	model = Reglas
	template_name = 'stakeholders/reglas/eliminar_regla.html'
	permission_required = 'stakeholders.delete_reglas'
	#success_url = reverse_lazy('stakeholders:ListarRegla')

	#enviar el token de seguridad y el metodo correcto que hay que usar es delete para el ajax
	def delete(self, request, pk, *args, **kwargs):
		if request.is_ajax():
			model = self.get_object()
			model.delete()
			mensaje = f'{self.model.__name__} eliminado correctamente!'
			error = 'No hay error!'
			response = JsonResponse({'mensaje': mensaje, 'error': error})
			response.status_code = 201
			return response
		else:
			return redirect('stakeholders:ListarRegla')

class ValidarInputReglaAjax(_ValidarInputAjax):
	model = Reglas
	permission_required = 'stakeholders.add_reglas'

class SearchActorAjax(_SearchNombreAjax):
	model = Actor
	permission_required = 'stakeholders.add_actor'