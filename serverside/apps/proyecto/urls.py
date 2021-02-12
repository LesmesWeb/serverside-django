from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
   
	#-----------------------------------------------------------------------------------------------
	# Proyecto ok
	#-----------------------------------------------------------------------------------------------
	
	path('lista',ListarProyectoFiltros.as_view(), name='lista_proyecto_filtros'), 
	path('crear/', CrearProyecto.as_view(), name = 'crear_proyecto'),
	path('buscar_tag/', SearchTagAjax.as_view(), name = 'buscar_tag'),
	path('editar/<int:pk>/', EditarProyecto.as_view(), name='editar_proyecto'),
	path('eliminar/<int:id>/', EliminarProyectoEstado.as_view(), name='eliminar_proyecto'),
	path('validar_input_proyecto/', ValidarInputNombreProyectoAjax.as_view(), name='validar_input_proyecto'),
	
	#-----------------------------------------------------------------------------------------------
	# Metodología ok
	#-----------------------------------------------------------------------------------------------
	
	path('metodologia/', ListarMetodologiaFiltros.as_view(), name='lista_metodologia'),
	path('metodologia/crear/', CrearMetodologia.as_view(), name = 'crear_metodologia'),
	path('metodologia/editar/<int:pk>/', EditarMetodologia.as_view(), name='editar_metodologia'),
	path('metodologia/eliminar/<int:id>/', EliminarMetodologia.as_view(), name='eliminar_metodologia'),
	path('validar_input_metodologia/', ValidarInputMetodologia.as_view(), name='validar_input_metodologia'),

]

