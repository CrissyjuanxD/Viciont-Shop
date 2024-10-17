from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.security.models import GroupModulePermission, Module, Group, Permission  # Asegúrate de importar correctamente los modelos
from app.security.forms.groupmodulepermission import GroupModulePermissionForm  # Asegúrate de importar correctamente el formulario GroupModulePermissionForm
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.contrib import messages
from django.db.models import Q

class GroupModulePermissionListView(PermissionMixin, ListViewMixin, ListView):
    model = GroupModulePermission
    template_name = 'security/groupmodulepermission/list.html'  # Asegúrate de tener esta ruta correcta según tu estructura de templates
    context_object_name = 'group_module_permissions'
    permission_required = 'view_groupmodulepermission'  # Define aquí el permiso requerido para ver la lista de GroupModulePermission
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query = Q(group__name__icontains=q) | Q(module__name__icontains=q)
        return GroupModulePermission.objects.filter(query).order_by('-id')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:groupmodulepermission_create')
        return context


class GroupModulePermissionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GroupModulePermission
    template_name = 'security/groupmodulepermission/form.html'
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy('security:groupmodulepermission_list')
    permission_required = 'add_groupmodulepermission'

    def form_valid(self, form):
        group = form.cleaned_data['group']
        # Eliminar todos los permisos actuales del grupo seleccionado
        GroupModulePermission.objects.filter(group=group).delete()
        
        modules_selected = self.request.POST.getlist('modules[]')
        for module_id in modules_selected:
            module = Module.objects.get(id=module_id)
            new_group_module_permission = GroupModulePermission.objects.create(
                group=group,
                module=module,
            )
            permissions_selected = self.request.POST.getlist(f'permissions_{module_id}[]')
            new_group_module_permission.permissions.set(permissions_selected)
        
        messages.success(self.request, "Permisos de grupo para los módulos seleccionados creados exitosamente.")
        return redirect(self.success_url)

    def get_group_permissions(self, group_id):
        all_modules = Module.objects.all()
        group_module_permissions = GroupModulePermission.objects.filter(group_id=group_id).select_related('module')
        assigned_modules = {gmp.module.id: list(gmp.permissions.values('id', 'name')) for gmp in group_module_permissions}
        
        permissions_data = []
        for module in all_modules:
            module_data = {
                'module_id': module.id,
                'module_name': module.name,
                'permissions': list(module.permissions.values('id', 'name')),
                'assigned_permissions': assigned_modules.get(module.id, [])
            }
            permissions_data.append(module_data)
        
        return JsonResponse(permissions_data, safe=False)



# class GroupModulePermissionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
#     model = GroupModulePermission
#     template_name = 'security/groupmodulepermission/form.html'
#     form_class = GroupModulePermissionForm
#     success_url = reverse_lazy('security:groupmodulepermission_list')
#     permission_required = 'change_groupmodulepermission'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         group_module_permission = self.get_object()

#         # Obtener todos los módulos y permisos
#         all_modules = Module.objects.all()
#         all_permissions = Permission.objects.all()

#         # Obtener los módulos y permisos actuales asociados a este GroupModulePermission
#         modules_permissions = []
#         for module in all_modules:
#             permissions = module.permissions.all()
#             modules_permissions.append({
#                 'module': module,
#                 'permissions': permissions,
#                 'selected_permissions': [permission.id for permission in permissions if permission in group_module_permission.permissions.all()]
#             })
        
#         context['modules_permissions'] = modules_permissions
#         context['group_module_permission'] = group_module_permission
#         return context

#     def get_initial(self):
#         initial = super().get_initial()
#         group_module_permission = self.get_object()
        
#         # Obtener los módulos y permisos asociados a este GroupModulePermission
#         initial['modules'] = [module.id for module in group_module_permission]
#         initial['permissions'] = [permission.id for permission in group_module_permission.permissions]
#         return initial

#     def get_object(self, queryset=None):
#         queryset = self.get_queryset()
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         return get_object_or_404(queryset, pk=pk)

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         context = self.get_context_data(object=self.object)
#         return self.render_to_response(context)

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         group_module_permission = form.save(commit=False)
#         group_module_permission.save()

#         # Limpiar los permisos existentes asociados a este GroupModulePermission
#         group_module_permission.permissions.clear()

#         modules_selected = self.request.POST.getlist('modules[]')
#         permissions_selected = self.request.POST.getlist('permissions[]')

#         for module_id in modules_selected:
#             module = Module.objects.get(id=module_id)
#             group_module_permission.module.add(module)
#             group_module_permission.permissions.add(*permissions_selected)

#         messages.success(self.request, f"Permisos de grupo para los módulos seleccionados actualizados exitosamente.")
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))

#     def get_queryset(self):
#         return GroupModulePermission.objects.filter(pk=self.kwargs.get('pk'))

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs.update({'user': self.request.user})  # Pasar el usuario al formulario si es necesario
#         return kwargs






class GroupModulePermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GroupModulePermission
    template_name = 'security/delete.html'  # Asegúrate de tener esta ruta correcta según tu estructura de templates
    success_url = reverse_lazy('security:groupmodulepermission_list')
    permission_required = 'delete_groupmodulepermission'  # Define aquí el permiso requerido para eliminar un GroupModulePermission
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, f"Permiso de grupo para módulo '{self.object.module.name}' eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = f"¿Está seguro que desea eliminar el permiso de grupo para el módulo '{self.object.module.name}'?"
        return context



def get_module_permissions(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
        permissions = list(module.permissions.values('id', 'name'))
        return JsonResponse(permissions, safe=False)
    except Module.DoesNotExist:
        return JsonResponse({'error': 'Module not found'}, status=404)