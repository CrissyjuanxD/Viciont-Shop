from django.forms import ModelForm
from django import forms
from app.security.models import Module, Menu  # Asegúrate de importar correctamente tu modelo Module y Menu desde tu aplicación

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['url', 'name', 'menu', 'description', 'icon', 'is_active', 'permissions']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL del módulo'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del módulo'}),
            'menu': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del módulo'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Icono del módulo'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permissions': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

        labels = {
            'url': 'URL',
            'name': 'Nombre',
            'menu': 'Menú',
            'description': 'Descripción',
            'icon': 'Icono',
            'is_active': '¿Es activo?',
            'permissions': 'Permisos',
        }
