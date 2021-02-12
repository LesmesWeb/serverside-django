"""serverside URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
#Permite establecer el template del login
from django.contrib.auth import views as auth_views
#Permite que las clases deban autenticarse para acceder
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de las apps
	path('stakeholders/',include(('apps.stakeholders.urls','stakeholders'))),
	path('proyecto/',include(('apps.proyecto.urls','proyecto'))),
    path('', login_required(TemplateView.as_view(template_name="index.html")),name='home'),
  
    #Autenticación
    path('accounts/', include('allauth.urls')), # new
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),


]

"""
Activamos el toolbar cuando el sistema tenga activado el debug y se encuentre en local
"""

from django.conf import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns