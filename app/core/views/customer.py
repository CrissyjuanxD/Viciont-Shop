from django.urls import reverse_lazy
from app.core.forms.customer import CustomerForm
from app.core.models import Customer
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

class CustomerListView(PermissionMixin, ListViewMixin, ListView):
    model = Customer
    template_name = 'core/customer/list.html'
    context_object_name = 'customer'
    permission_required = 'view_customer'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q')
        query = Q()
        if q1 is not None:
            query.add(Q(first_name__icontains=q1) | Q(last_name__icontains=q1) | Q(dni__icontains=q1), Q.OR)
        return self.model.objects.filter(query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:customer_create')
        return context

class CustomerCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Customer
    template_name = 'core/customer/form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'add_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Cliente'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        customer = self.object
        messages.success(self.request, f"Éxito al crear el cliente {customer.get_full_name}.")
        return response
    
class CustomerUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Customer
    template_name = 'core/customer/form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'change_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Cliente'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        customer = self.object
        messages.success(self.request, f"Éxito al actualizar el cliente {customer.get_full_name}.")
        return response
    
class CustomerDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Customer
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'delete_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Cliente'
        context['description'] = f"¿Desea eliminar el cliente: {self.object.get_full_name}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Llama al método delete() del modelo que realiza un borrado lógico
        success_message = f"Éxito al eliminar lógicamente el cliente {self.object.get_full_name}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
