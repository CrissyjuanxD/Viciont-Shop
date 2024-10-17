from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from app.security.models import User
from django.contrib import messages
from django.shortcuts import redirect



class CustomPasswordResetView(PasswordResetView):
    template_name = 'security/auth/recuperacion_contra/password_reset_form.html'
    email_template_name = 'security/auth/recuperacion_contra/password_reset_email.html'
    success_url = reverse_lazy('security:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return super().form_valid(form)
        else:
            messages.error(self.request, "No hay una cuenta asociada con ese correo electrónico.")
            return redirect('security:reset_password')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'security/auth/recuperacion_contra/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'security/auth/recuperacion_contra/password_reset_confirm.html'
    success_url = reverse_lazy('security:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'security/auth/recuperacion_contra/password_reset_complete.html'
