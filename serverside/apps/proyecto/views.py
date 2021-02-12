import json 
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist (TRY CASH)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse,JsonResponse
from django.views.generic import View,ListView,UpdateView,CreateView,DeleteView

from .models import Proyecto,Metodologia,Tag

from .forms import FormCreateProyecto,FormCreateMetodologia
from .filters import ProyectoFilter,MetodologiaFilter


"""
---------------- Clases practicas para reutilizar  -------
"""

class _FormValid(PermissionRequiredMixin):
	model = Proyecto
	permission_required = 'proyecto.add_proyecto'
	form_class = FormCreateProyecto
	template_name = 'proyecto/proyecto/crear_proyecto.html'
	success_url = reverse_lazy('proyecto:lista_proyecto_filtros')
	success_message = 'Se ha creado con éxito'
	error_message = 'No se guardo con exito.'

	def form_valid(self, form):
		#form.instance.created_by = self.request.user
		messages.success(self.request, self.success_message, extra_tags='God Job')
		return super().form_valid(form)

	def form_invalid(self, form):
		lista = ""
		for error in form.errors:
			lista+=str(error)
		#https://stackoverflow.com/questions/43588876/how-can-i-add-additional-data-to-django-messages
		messages.error(self.request, '%s debido a un error en el campo de: %s' % (self.error_message, lista), extra_tags='Error')
		return redirect(str(self.success_url))

	#Validación que limpia el los input de un espacio inicial y final con strip al guardar
	#https://www.peterbe.com/plog/automatically-strip-whitespace-in-django-forms
	def clean(self):
		for field in self.cleaned_data:
			if isinstance(self.cleaned_data[field], basestring):
				self.cleaned_data[field] = self.cleaned_data[field].strip()
		return self.cleaned_data
		
class _FormValidFiltros(PermissionRequiredMixin,ListView):
	model = Proyecto
	permission_required = 'proyecto.add_proyecto'
	template_name = 'proyecto/proyecto/crear_proyecto.html'
	filter_class = ProyectoFilter #https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/
	form_class = FormCreateProyecto

	def get_queryset(self):
		qs = self.model.objects.all()
		product_filtered_list = self.filter_class(self.request.GET, queryset=qs)
		return product_filtered_list.qs,product_filtered_list #Django Filter (https://riptutorial.com/es/django/example/21255/utilice-django-filter-con-cbv)

	def get_context_data(self,**kwargs):
		contexto = {}
		#contexto = super().get_context_data(**kwargs)
		object_list,myfilter= self.get_queryset() #retornar elementos de una función por tupla (https://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/)
		contexto['object_list'] = object_list
		contexto['myfilter'] = myfilter
		contexto['form'] = self.form_class
		return contexto

class _CrearFormValid(_FormValid,CreateView):
	model = Metodologia
	permission_required = 'proyecto.add_metologia'
	form_class = FormCreateMetodologia
	template_name = 'proyecto/metodologia/crear_metodologia.html'
	success_url = reverse_lazy('proyecto:lista_metodologia')
	
	def post(self, request, *args, **kwargs):
		
		#cargo los datos del formulario
		form = self.form_class(request.POST)
		print("entro a post ")
		if form.is_valid():
			print("validado")
			form.save()
			return self.form_valid(form)

		#De lo contratio que muestre error
		else:
			print("in validado")
			self.form_invalid(form)
			
		return redirect(str(self.success_url))

class _EliminarPermanentemente(_FormValid,DeleteView):
	model = Metodologia
	permission_required = 'proyecto.delete_metodologia'
	success_url = reverse_lazy('proyecto:lista_metodologia')
	success_message = 'La metodología fue eliminada con éxito'

	"""
		def get_object(self):
			id_= self.kwargs.get("id")
			return get_object_or_404(self.model, id=id_)
	"""

	def get(self, request, *args, **kwargs):
		#model_query = self.model.objects.get(id = kwargs['id'])
		print("kwargs['id'] ",type(kwargs['id']))
		obj = get_object_or_404(self.model, pk = kwargs['id'])
		obj.delete()
		messages.success(self.request, self.success_message, extra_tags='God Job')
		return redirect(str(self.success_url))

class _EliminarCambiandoEstado(_FormValid,DeleteView):
	permission_required = 'proyecto.delete_proyecto'
	model = Proyecto
	success_url =  reverse_lazy('proyecto:lista_proyecto_filtros')
	success_message = 'Proyecto desactivado correctament'
	error_message = 'No se desactivado con exito.'

	def get(self, request, *args, **kwargs):
		obj = get_object_or_404(self.model, pk = kwargs['id'])
		print("obj.estado --> ",obj.estado)
		if obj.estado:
			obj.estado = False
			obj.save()
			messages.success(self.request, self.success_message, extra_tags='God Job')
		elif obj.estado == False:
			messages.info(self.request, 'Ya se encuentra desactivado')
		else:
			messages.error(self.request, self.error_message, extra_tags='Error')
			
		return redirect(str(self.success_url))


#AJAX

class _ValidarInputAjax(PermissionRequiredMixin,View):
	model = Proyecto
	permission_required = 'proyecto.add_proyecto'

	def post(self, request, *args, **kwargs):
		nombre_input = request.POST.get('nombre_data_ajax')
		#print("validar datos de envio --> ",dict(request.POST.lists()))
		if self.model.objects.filter(nombre__iexact=nombre_input).exists():
			valido = True
		else:
			valido = False
		print("valido --> ",valido)

		return HttpResponse(json.dumps({'valido': valido}), content_type='application/json')

class _SearchNombreAjax(PermissionRequiredMixin,CreateView):
	model = Tag
	permission_required = 'proyecto.add_proyecto'

	def get(self, request, *args, **kwargs):
		
		data = request.GET.dict()
		query = self.model.objects.filter(nombre__istartswith=data['term']).values('id','nombre')
		data_dict_result= []
		
		for i in query:
			data_list= {
				'id' : i['id'],
				'name' : i['nombre']
			}
			data_dict_result.append(data_list)
			print("data_dict_result --> ",data_dict_result)
		return  JsonResponse(data_dict_result, safe=False)


"""
---------------- Proyecto-------
"""

class ListarProyectoFiltros(_FormValidFiltros):
	model = Proyecto
	form_class = FormCreateProyecto
	template_name = 'proyecto/proyecto/listar_proyecto_filtros.html'
	permission_required = 'proyecto.view_proyecto'

	def get_queryset(self):
		qs = self.model.objects.all().prefetch_related('director').prefetch_related('colaborador').prefetch_related('metodologia')
		product_filtered_list = ProyectoFilter(self.request.GET, queryset=qs)
		return product_filtered_list.qs,product_filtered_list #Django Filter (https://riptutorial.com/es/django/example/21255/utilice-django-filter-con-cbv)

class CrearProyecto(_FormValid,CreateView):
	model = Proyecto
	permission_required = 'proyecto.add_proyecto'
	form_class = FormCreateProyecto
	template_name = 'proyecto/proyecto/crear_proyecto.html'
	success_url = reverse_lazy('proyecto:lista_proyecto_filtros')
	success_message = 'el Proyecto fue creado con éxito'
	error_message = 'No se guardo con exito.'

	def get_queryset(self):
		queryset = self.model.objects.all().prefetch_related('director').prefetch_related('colaborador').prefetch_related('metodologia')
		return queryset 

	def post(self, request, *args, **kwargs):
		
		#Llamo los datos recibidos en post y los convierto en lista para tenerlos datos del ajax de tags
		form_header = dict(request.POST.lists())

		#Valido si contiene información para realizar el filtro
		if 'tags' in form_header:
			#capturo los ids de tags (manytomany)
			tag_query = Tag.objects.filter(pk__in=form_header['tags']) 
		else:
			#sino capturo todo los valores
			tag_query = Tag.objects.none()
			pass
				
		#cargo los datos del formulario
		form = self.form_class(request.POST)

		#se asigno el query al formulario
		form.fields['tags'].queryset = tag_query

		#Valido el formulario y si cumple que guarde y notifique con SweetAlert el guardado
		if form.is_valid():
			form.save()
			return self.form_valid(form)

		#De lo contratio que muestre error
		else:
			self.form_invalid(form)
			
		return redirect(str(self.success_url))

class EditarProyecto(_FormValid,UpdateView):
	model = Proyecto
	permission_required = 'proyecto.change_proyecto'
	form_class = FormCreateProyecto
	template_name = 'proyecto/proyecto/editar_proyecto.html'
	success_url = reverse_lazy('proyecto:lista_proyecto_filtros')
	success_message = 'el Proyecto fue editado con éxito'
	error_message = 'No se edito con exito.'

	# Solución al n+1
	def get_queryset(self):
		queryset = self.model.objects.all().prefetch_related('director').prefetch_related('colaborador').prefetch_related('metodologia')
		return queryset 

	# Devuelve la instacia del formulario lista
	def get_form(self,*args,**kwargs):
		instance = self.get_object() 
		form = self.form_class(instance=instance)
		print("instance editar query: ",instance.tags)
		form.fields['tags'].queryset = instance.tags.all()
		print("get form", form.fields['tags'].queryset)
		#print("instance ---> ",instance) #nombre del campo
		#print("form.fields['tags'] --> ",form.fields['tags'].queryset) #<QuerySet [<Tag: asdsad>, <Tag: prueba 2>]>
		return form
	
	def get(self,*args,**kwargs):
		context = {}
		context["form"] = self.get_form()
		context["id_proyecto"] = self.kwargs.get("pk",None) #Reemplazo el object.id
		return render(self.request,self.template_name,context, self.get_form)

	def post(self, request, *args, **kwargs):
		
		#Llamo los datos recibidos en post y los convierto en lista para tenerlos datos del ajax de tags
		form_header = dict(request.POST.lists())

		if 'tags' in form_header:
			#print(form_header['tags']) ['1', '3']
			tag_query = Tag.objects.filter(pk__in=form_header['tags']) 
		else:
			#sino capturo todo los valores
			tag_query = Tag.objects.none()
			pass

		print("self.kwargs.get(pk,None) ",self.kwargs.get("pk",None))
		obj = get_object_or_404(self.model, id = self.kwargs.get("pk",None))

		# pasamos el objeto como una instancia
		form = self.form_class(request.POST or None, instance = obj)

		#se asigno el query al formulario
		form.fields['tags'].queryset = tag_query

		#Valido el formulario y si cumple que guarde y notifique con SweetAlert el guardado
		if form.is_valid():
			print("valido primo")
			form.save()
			return self.form_valid(form)
		else:
			self.form_invalid(form)

		return redirect('proyecto:lista_proyecto_filtros')

class EliminarProyectoEstado(_EliminarCambiandoEstado):
	pass

class SearchTagAjax(_SearchNombreAjax):
	pass

class ValidarInputNombreProyectoAjax(_ValidarInputAjax):
	pass

"""
---------------- Metodología -------
"""

class ListarMetodologiaFiltros(_FormValidFiltros):
	model = Metodologia
	form_class = FormCreateMetodologia
	template_name = 'proyecto/metodologia/listar_metodologia_filtros.html'
	permission_required = 'proyecto.view_metodologia'
	filter_class = MetodologiaFilter

class CrearMetodologia(_CrearFormValid):
	pass

class EditarMetodologia(_FormValid,UpdateView):
	model = Metodologia
	permission_required = 'proyecto.change_metodologia'
	form_class = FormCreateMetodologia
	template_name = 'proyecto/metodologia/editar_metodologia.html'
	success_url = reverse_lazy('proyecto:lista_metodologia')

class EliminarMetodologia(_EliminarPermanentemente):
	pass

class ValidarInputMetodologia(_ValidarInputAjax):
	model = Metodologia
	permission_required = 'proyecto.add_metodologia'
