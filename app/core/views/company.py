from django.urls import reverse_lazy
from app.core.forms.company import CompanyForm
from app.core.models import Company
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

class CompanyListView(PermissionMixin, ListViewMixin, ListView):
    model = Company
    template_name = 'core/company/list.html'
    context_object_name = 'company'
    permission_required = 'view_company'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q')
        query = Q()
        if q1 is not None:
            query.add(Q(name__icontains=q1), Q.OR)
        return self.model.objects.filter(query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:company_create')
        return context

class CompanyCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Company
    template_name = 'core/company/form.html'
    form_class = CompanyForm
    success_url = reverse_lazy('core:company_list')
    permission_required = 'add_company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Compañía'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        company = self.object
        messages.success(self.request, f"Éxito al crear la compañía {company.name}.")
        return response
    
class CompanyUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Company
    template_name = 'core/company/form.html'
    form_class = CompanyForm
    success_url = reverse_lazy('core:company_list')
    permission_required = 'change_company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Compañía'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        company = self.object
        messages.success(self.request, f"Éxito al actualizar la compañía {company.name}.")
        return response
    
class CompanyDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Company
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:company_list')
    permission_required = 'delete_company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Compañía'
        context['description'] = f"¿Desea eliminar la compañía: {self.object.name}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Llama al método delete() del modelo que realiza un borrado lógico
        success_message = f"Éxito al eliminar lógicamente la compañía {self.object.name}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
