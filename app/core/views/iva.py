from django.urls import reverse_lazy
from app.core.forms.iva import IvaForm
from app.core.models import Iva
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

class IvaListView(PermissionMixin, ListViewMixin, ListView):
    model = Iva
    template_name = 'core/iva/list.html'
    context_object_name = 'iva'
    permission_required = 'view_iva'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q')
        query = Q()
        if q1 is not None:
            query.add(Q(description__icontains=q1), Q.OR)
        return self.model.objects.filter(query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:iva_create')
        return context

class IvaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Iva
    template_name = 'core/iva/form.html'
    form_class = IvaForm
    success_url = reverse_lazy('core:iva_list')
    permission_required = 'add_iva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar IVA'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        iva = self.object
        messages.success(self.request, f"Éxito al crear el IVA {iva.description}.")
        return response
    
class IvaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Iva
    template_name = 'core/iva/form.html'
    form_class = IvaForm
    success_url = reverse_lazy('core:iva_list')
    permission_required = 'change_iva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar IVA'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        iva = self.object
        messages.success(self.request, f"Éxito al actualizar el IVA {iva.description}.")
        return response
    
class IvaDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Iva
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:iva_list')
    permission_required = 'delete_iva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar IVA'
        context['description'] = f"¿Desea eliminar el IVA: {self.object.description}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Llama al método delete() del modelo que realiza un borrado lógico
        success_message = f"Éxito al eliminar lógicamente el IVA {self.object.description}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
