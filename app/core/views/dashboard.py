from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import PermissionMixin
from django.views.generic import TemplateView
from app.sales.models import Invoice  

class ChartTemplateView(UserPassesTestMixin, PermissionMixin, TemplateView):
    template_name = 'components/homepro.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "CS - Gráficos"
        context["title2"] = "Visualización de Datos"
        MenuModule(self.request).fill(context)
        sales_data = Invoice.objects.all().values('month', 'total_sales')  
        context['sales_data'] = list(sales_data)  
        
        return context

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect(reverse('no_permission'))
