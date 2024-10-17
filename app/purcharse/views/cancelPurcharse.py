from django.urls import reverse_lazy
from app.core.forms.supplier import SupplierForm
from app.core.models import Product
from app.sales.forms.invoice import InvoiceForm
from app.sales.models import Invoice
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q,F

from django.urls import reverse_lazy
from app.core.models import Supplier
from app.purcharse.forms.compra import PurchaseForm
from app.purcharse.models import Purchase
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

class PurchaseListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'shop.html'  # Asegúrate de usar el nombre correcto de tu template
    model = Purchase
    context_object_name = 'purchases'
    permission_required = 'view_purchase'  # Ajusta según tus permisos

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            return self.model.objects.filter(
                Q(num_document__icontains=q1) |
                Q(supplier__name__icontains=q1)
            ).order_by('-issue_date')
        return self.model.objects.all().order_by('-issue_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir cualquier contexto adicional que necesites
        return context

class PurchaseCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Purchase
    template_name = 'shopping_list.html'  # Asegúrate de usar el nombre correcto de tu template
    form_class = PurchaseForm
    success_url = reverse_lazy('sales:purchase_list')  # Ajusta según tus URLs
    permission_required = 'add_purchase'  # Ajusta según tus permisos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()  # Ajusta según tus necesidades
        # Añadir cualquier otro contexto necesario
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        purchase = self.object
        messages.success(self.request, f"Compra registrada exitosamente con número de documento {purchase.num_document}.")
        return response


class PurchaseUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Purchase
    template_name = 'shopping_card.html'  # Asegúrate de usar el nombre correcto de tu template
    form_class = PurchaseForm
    success_url = reverse_lazy('sales:purchase_list')  # Ajusta según tus URLs
    permission_required = 'change_purchase'  # Ajusta según tus permisos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()  # Ajusta según tus necesidades
        # Añadir cualquier otro contexto necesario
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        purchase = self.object
        messages.success(self.request, f"Compra actualizada exitosamente con número de documento {purchase.num_document}.")
        return response


class PurchaseDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Purchase
    template_name = 'shopping_card.html'  # Asegúrate de usar el nombre correcto de tu template
    success_url = reverse_lazy('sales:purchase_list')  # Ajusta según tus URLs
    context_object_name = 'purchase'
    permission_required = 'delete_purchase'  # Ajusta según tus permisos

    def delete(self, request, *args, **kwargs):
        purchase = self.get_object()
        messages.success(self.request, f"Compra eliminada exitosamente con número de documento {purchase.num_document}.")
        return super().delete(request, *args, **kwargs)



