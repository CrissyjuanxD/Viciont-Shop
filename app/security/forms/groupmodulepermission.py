from django import forms
from app.security.models import GroupModulePermission, Module
from django.forms import ModelForm

class GroupModulePermissionForm(ModelForm):
    class Meta:
        model = GroupModulePermission
        fields = ['group']
        widgets = {
            'group': forms.Select(attrs={"class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"}),  # Aquí puedes ajustar las clases de Tailwind
        }

        labels = {
            'group': 'Grupo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['module'] = forms.ModelMultipleChoiceField(
            queryset=Module.objects.filter(is_active=True),
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
            required=False
        )
