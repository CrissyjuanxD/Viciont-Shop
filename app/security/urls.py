from django.urls import path
from app.security.views import auth, menu, module, groupmodulepermission, password_reset
app_name = "security"
urlpatterns = []
# security
urlpatterns += [
    path('auth/login',auth.signin,name="auth_login"),
    path('auth/signup',auth.signup,name="auth_signup"),
    path('auth/logout',auth.signout,name='auth_logout'),
    path('auth/profile',auth.profile,name='auth_profile'),
    path('auth/update_profile',auth.update_profile,name='auth_update_profile'),
    path('auth/update_contra' , auth.actulizarcontra, name='auth_update_contra'),
        # URLs de Menús
    path('menu_list/', menu.MenuListView.as_view(), name='menu_list'),
    path('menu_create/', menu.MenuCreateView.as_view(), name='menu_create'),
    path('menu_update/<int:pk>/', menu.MenuUpdateView.as_view(), name='menu_update'),
    path('menu_delete/<int:pk>/', menu.MenuDeleteView.as_view(), name='menu_delete'),
    
        # URLs de Módulos
    path('module_list/', module.ModuleListView.as_view(), name='module_list'),
    path('module_create/', module.ModuleCreateView.as_view(), name='module_create'),
    path('module_update/<int:pk>/', module.ModuleUpdateView.as_view(), name='module_update'),
    path('module_delete/<int:pk>/', module.ModuleDeleteView.as_view(), name='module_delete'),
    
        # URLs de Grupos Módulos Permisos
    path('groupmodulepermission_list/', groupmodulepermission.GroupModulePermissionListView.as_view(), name='groupmodulepermission_list'),
    path('groupmodulepermission_create/', groupmodulepermission.GroupModulePermissionCreateView.as_view(), name='groupmodulepermission_create'),
    #path('groupmodulepermission_update/<int:pk>/', groupmodulepermission.GroupModulePermissionUpdateView.as_view(), name='groupmodulepermission_update'),
    path('groupmodulepermission_delete/<int:pk>/', groupmodulepermission.GroupModulePermissionDeleteView.as_view(), name='groupmodulepermission_delete'),
    path('get_module_permissions/<int:module_id>/', groupmodulepermission.get_module_permissions, name='get_module_permissions'),
    path('get_group_permissions/<int:group_id>/', groupmodulepermission.GroupModulePermissionCreateView.get_group_permissions, name='get_group_permissions'),
    
        # Recuperar contraseñan olvidada
    path('reset_password/', password_reset.CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', password_reset.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', password_reset.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

