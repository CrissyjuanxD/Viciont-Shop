from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.security.models import User
from django.forms import ImageField, FileInput
from django.contrib.auth.forms import UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    image = forms.ImageField(required=False)  # Marcamos la imagen como no obligatoria

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'dni', 'direction', 'phone', 'image')
class CustomUserUpdateForm(UserChangeForm):
    password = None  # No incluir el campo de contraseña

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'dni', 'direction', 'phone', 'image')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
class CustomUserUpdateForm(UserChangeForm):
    password = None  # No incluir el campo de contraseña

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'dni', 'direction', 'phone', 'image')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Por favor, sube una imagen válida (jpg, jpeg, png).")
        return image

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password1 != new_password2:
            raise forms.ValidationError("Las contraseñas nuevas no coinciden.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
