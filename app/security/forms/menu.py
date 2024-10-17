from django.forms import ModelForm
from django import forms
from app.security.models import Menu  # Asegúrate de importar correctamente tu modelo Menu desde tu aplicación

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'icon']  # Campos que deseas mostrar en el formulario

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del menú'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Icono del menú'}),
        }

        labels = {
            'name': 'Nombre',
            'icon': 'Icono',
        }
