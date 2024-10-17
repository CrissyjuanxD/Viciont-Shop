from django.urls import reverse_lazy
from django.db.models.deletion import ProtectedError
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.security.models import Menu, Module
from django.shortcuts import redirect, render
from app.security.forms.menu import MenuForm
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.contrib import messages
from django.db.models import Q

class MenuListView(PermissionMixin, ListViewMixin, ListView):
    model = Menu
    template_name = 'security/menu/list.html'  # Asegúrate de tener esta ruta correcta según tu estructura de templates
    context_object_name = 'menus'
    permission_required = 'view_menu'  # Define aquí el permiso requerido para ver la lista de menús
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query = Q(name__icontains=q)
        return Menu.objects.filter(query).order_by('-name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:menu_create')
        return context

class MenuCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Menu
    template_name = 'security/menu/form.html'  # Asegúrate de tener esta ruta correcta según tu estructura de templates
    form_class = MenuForm
    success_url = reverse_lazy('security:menu_list')
    permission_required = 'add_menu'  # Define aquí el permiso requerido para crear un menú
    
    def form_valid(self, form):
        response = super().form_valid(form)
        menu = self.object
        messages.success(self.request, f"Menú '{menu.name}' creado exitosamente.")
        return response

class MenuUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Menu
    template_name = 'security/menu/form.html'  # Asegúrate de tener esta ruta correcta según tu estructura de templates
    form_class = MenuForm
    success_url = reverse_lazy('security:menu_list')
    permission_required = 'change_menu'  # Define aquí el permiso requerido para actualizar un menú
    
    def form_valid(self, form):
        response = super().form_valid(form)
        menu = self.object
        messages.success(self.request, f"Menú '{menu.name}' actualizado exitosamente.")
        return response



class MenuDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Menu
    template_name = 'security/delete.html'
    success_url = reverse_lazy('security:menu_list')
    permission_required = 'delete_menu'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        modules_linked = Module.objects.filter(menu=self.object)
        
        if modules_linked.exists():
            messages.warning(self.request, f"Para eliminar el Menú '{self.object.name}' primero elimine los siguientes módulos: {[module.name for module in modules_linked]}.")
            return redirect('security:menu_list')
        else:
            messages.success(self.request, f"Menú '{self.object.name}' eliminado exitosamente.")
            return super().post(request, *args, **kwargs)
            
            