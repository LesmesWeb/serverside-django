from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .views_ajax import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .filters import ActorFilter

urlpatterns = [

	#-----------------------------------------------------------------------------------------------
	#Reglas ok
	#-----------------------------------------------------------------------------------------------
	
	path('reglas/',ListarReglaAjax.as_view(),{'parametro_extra':"Listado Reglas"},name='ListarRegla'),
	path('crear_regla/', CrearReglaAjax.as_view(),name='CrearRegla'),
	path('editar_regla/<int:pk>/', EditarReglaAjax.as_view(), name = 'EditarRegla'),
	path('eliminar_regla/<int:pk>/', EliminarReglaAjax.as_view(), name = 'EliminarRegla'),
	path('validar_input_regla/', ValidarInputReglaAjax.as_view(), name='validar_input_regla'),
	path('buscar_actor/', SearchActorAjax.as_view(), name = 'buscar_actor'),

	#-----------------------------------------------------------------------------------------------
	#Actor ok
	#-----------------------------------------------------------------------------------------------
	
	path('actor', ListarActor.as_view(), name='ListarActor'),
	path('crear_actor/', CrearActor.as_view(),name='CrearActor'),
	path('editar_actor/<int:pk>/', EditarActor.as_view(), name = 'EditarActor'),
	path('eliminar_actor/<int:id>/', EliminarActor.as_view(), name = 'EliminarActor'),
	path('eliminar_actor_estado/<int:pk>/', EliminarActorEstado.as_view(), name = 'EliminarActorEstado'),
	path('validar_input_actor/', ValidarInputActor.as_view(), name='validar_input_actor'),

]

# url de vistas implicitas (que solo se definen por parametros)
urlpatterns += [
	path('reglas_inicio/',login_required(
		TemplateView.as_view(
			template_name = 'stakeholders/reglas/listar_reglas.html'
		)
	), name='reglas_inicio'),

]
	

