from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.security.models import Module, GroupModulePermission  # Asegúrate de importar correctamente el modelo Module
from app.security.forms.module import ModuleForm  # Asegúrate de importar correctamente el formulario ModuleForm
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.contrib import messages
from django.db.models import Q

class ModuleListView(PermissionMixin, ListViewMixin, ListView):
    model = Module
    template_name = 'security/module/list.html'  # Asegúrate de tener esta ruta correcta según tu estructura de templates
    context_object_name = 'modules'
    permission_required = 'view_module'  # Define aquí el permiso requerido para ver la lista de módulos
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query = Q(name__icontains=q)
        return Module.objects.filter(query).order_by('-name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:module_create')
        return context

class ModuleCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Module
    template_name = 'security/module/form.html'  # Asegúrate de tener esta ruta correcta según tu estructura de templates
    form_class = ModuleForm
    success_url = reverse_lazy('security:module_list')
    permission_required = 'add_module'  # Define aquí el permiso requerido para crear un módulo
    
    def form_valid(self, form):
        response = super().form_valid(form)
        module = self.object
        messages.success(self.request, f"Módulo '{module.name}' creado exitosamente.")
        return response

class ModuleUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Module
    template_name = 'security/module/form.html'  # Asegúrate de tener esta ruta correcta según tu estructura de templates
    form_class = ModuleForm
    success_url = reverse_lazy('security:module_list')
    permission_required = 'change_module'  # Define aquí el permiso requerido para actualizar un módulo
    
    def form_valid(self, form):
        response = super().form_valid(form)
        module = self.object
        messages.success(self.request, f"Módulo '{module.name}' actualizado exitosamente.")
        return response


class ModuleDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Module
    template_name = 'security/delete.html'
    success_url = reverse_lazy('security:module_list')
    permission_required = 'delete_module'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        groupmodulepermissions_linked = GroupModulePermission.objects.filter(module=self.object)
        if groupmodulepermissions_linked.exists():
            messages.warning(self.request, f"Para eliminar el Módulo '{self.object.name}' primero elimine los siguientes grupos modulos permisos vinculados: {[gmp.module.name + ' - ' +  gmp.group.name for gmp in groupmodulepermissions_linked]}.")
            return redirect('security:module_list')
        else:
            messages.success(self.request, f"Módulo '{self.object.name}' eliminado exitosamente.")
            return super().post(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['description'] = f"¿Está seguro que desea eliminar el módulo '{self.object.name}'?"
    #     return context