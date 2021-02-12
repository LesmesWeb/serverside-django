# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from .models import Actor,Reglas

class ActorForm(forms.ModelForm):
	class Meta:
		model = Actor
		fields = ('nombre','genero','alias','es_autor','email','es_medio','es_persona','es_organizacion')
		widgets = {   
			'nombre':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Ingrese el Titular del Articulo',
					'id':'nombre'
				}
				
			),
			'genero':forms.Select(
				attrs={
					'class': 'activate_select_one form-control',
					'id':'genero',
				}
			),
			'alias':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Ingrese el Titular del Articulo',
					'id':'alias'
				}
				
			),
			'es_autor':forms.CheckboxInput(),

			'email':forms.TextInput(
				attrs={
					'class':'form-control',
					'type':'email',
					'placeholder':'Ingrese el Titular del Articulo',
					'id':'nombre'
				}
				
			),
			'es_medio':forms.CheckboxInput(),
			'es_persona':forms.CheckboxInput(),
			'es_organizacion':forms.CheckboxInput(),
		}



class ReglasFormCrear(forms.ModelForm):
	class Meta:
		model = Reglas
		fields = ['actor','nombre']

		widgets = {
			'actor':forms.Select(
				attrs={
					'class':'form-control',
					'placeholder':'Ingrese el Cargo',
					'id':'actor_crear'
				}
			),
			'nombre':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Ingrese el Cargo',
					'id':'nombre_crear'
				}
			),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['actor'].queryset = Actor.objects.none()

class ReglasFormEditar(forms.ModelForm):
	class Meta:
		model = Reglas
		fields = ['actor','nombre']

		widgets = {
			'actor':forms.Select(
				attrs={
					'class':'form-control',
					'placeholder':'Ingrese el Cargo',
					'id':'actor_editar'
				}
			),
			'nombre':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Ingrese el Cargo',
					'id':'nombre_editar'
				}
			),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['actor'].queryset = Actor.objects.none()
