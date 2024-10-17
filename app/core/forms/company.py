from django.forms import ModelForm
from django import forms
from app.core.models import Company

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "dni", "name", "address", "representative", "landline", "website", "email", 
            "logo", "establishment_code", "emission_point_code", "authorization_number", 
            "taxpayer_type", "required_to_keep_accounting", "economic_activity_code"
        ]
        error_messages = {
            "name": {
                "unique": "Ya existe una empresa con este nombre.",
            },
        }
        widgets = {
            "dni": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese RUC",
                    "id": "id_dni",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese nombre de la empresa",
                    "id": "id_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese dirección de la empresa",
                    "id": "id_address",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "representative": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese nombre del responsable",
                    "id": "id_representative",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "landline": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese teléfono fijo",
                    "id": "id_landline",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "placeholder": "Ingrese sitio web de la empresa",
                    "id": "id_website",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Ingrese correo electrónico de la empresa",
                    "id": "id_email",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "logo": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "id_logo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "establishment_code": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese código de establecimiento",
                    "id": "id_establishment_code",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "emission_point_code": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese código de punto de emisión",
                    "id": "id_emission_point_code",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "authorization_number": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese número de autorización",
                    "id": "id_authorization_number",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "taxpayer_type": forms.Select(
                attrs={
                    "id": "id_taxpayer_type",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "required_to_keep_accounting": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "economic_activity_code": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese código de actividad económica",
                    "id": "id_economic_activity_code",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "dni": "RUC",
            "name": "Empresa",
            "address": "Dirección",
            "representative": "Responsable",
            "landline": "Teléfono Fijo",
            "website": "Sitio Web",
            "email": "Correo Electrónico",
            "logo": "Logo",
            "establishment_code": "Código de Establecimiento",
            "emission_point_code": "Código de Punto de Emisión",
            "authorization_number": "Número de Autorización",
            "taxpayer_type": "Tipo de Contribuyente",
            "required_to_keep_accounting": "Obligado a Llevar Contabilidad",
            "economic_activity_code": "Código de Actividad Económica",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.upper()
