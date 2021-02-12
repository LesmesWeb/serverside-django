# -*- coding: utf-8 -*-
from django import forms
from .models import *

class FormCreateProyecto(forms.ModelForm):

	class Meta:
		TRUE_FALSE_CHOICES = (
			('', 'Todos..'),
			(True, 'Activo'),
			(False, 'Inactivo')
		)

		model = Proyecto
		fields=['nombre','link_powerbi','meta','director','colaborador','metodologia', 'estado','descripcion','tipo_prediccion','tags']
		widgets = {

			'link_powerbi':forms.Textarea(
				attrs={
					'class':'form-control',
					#'placeholder':'Ingrese el Nombre del Proyecto',
					'type':'url',
					'id':'link_powerbi',
					'name':'link_powerbi',
					'rows':'5',
				}
				
			),

			'meta':forms.TextInput(
				attrs={
					'type':'number',
					'class':'form-control',
				}
			),

			
			'descripcion':forms.Textarea(
				attrs={
					'class':'form-control',
					#'placeholder':'Ingrese el Nombre del Proyecto',
					'type':'url',
					'id':'descripcion',
					'name':'descripcion',
					'rows':'6',
				}
				
			),

		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['tags'].queryset = Tag.objects.none()

class FormCreateMetodologia(forms.ModelForm):

	class Meta:
		model = Metodologia
		fields=['nombre',]

		widgets = {
			'nombre':forms.Textarea(
				attrs={
					'class':'form-control',
					#'placeholder':'Ingrese el Nombre del Proyecto',
					'id':'nombre_metodologia_input',
					'rows':'8',
				}
				
			),

		}