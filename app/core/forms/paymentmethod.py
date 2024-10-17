from django.forms import ModelForm
from django import forms
from app.core.models import PaymentMethod

class PaymentMethodForm(ModelForm):
    class Meta:
        model = PaymentMethod
        fields = [
            "description", "image", "active"
        ]
        error_messages = {
            "description": {
                "unique": "Ya existe un método de pago con esta descripción.",
            },
        }
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese descripción del método de pago",
                    "id": "id_description",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "id_image",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
        }
        labels = {
            "description": "Descripción",
            "image": "Foto",
            "active": "Activo",
        }

    def clean_description(self):
        description = self.cleaned_data.get("description")
        return description.upper()
