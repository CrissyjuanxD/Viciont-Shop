from django.urls import reverse_lazy
from app.core.models import Product, Supplier
from app.purcharse.forms.compra import PurchaseForm
from app.purcharse.models import Purchase, PurchaseDetail
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from app.core.models import Product
import json

class PurchaseListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'purchase/shop.html'  # Asegúrate de usar el nombre correcto de tu template
    model = Purchase
    context_object_name = 'purchases'
    permission_required = 'view_purchase'

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
        # Añadir cualquier contexto adicional necesario
        
        context['products'] = Product.objects.all()  # Añadir los productos al contexto
        context['title1'] = 'Productos Disponibles'
        context['title2'] = 'Lista de Productos'
        return context
    
    
class PurchaseCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Purchase
    template_name = 'purchase/shopping_list.html'  # Asegúrate de usar el nombre correcto de tu template
    form_class = PurchaseForm
    success_url = reverse_lazy('sales:purchase_list')
    permission_required = 'add_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()  # Ajusta según tus necesidades
        # Añadir cualquier otro contexto necesario
        # context['products'] = Product.objects.all()
        # context['title1'] = 'Productos Disponibles'
        # context['title2'] = 'Lista de Productos'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        purchase = self.object
        messages.success(self.request, f"Compra registrada exitosamente con número de documento {purchase.num_document}.")
        return response

class PurchaseUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Purchase
    template_name = 'purchase/shopping_cart.html'  # Asegúrate de usar el nombre correcto de tu template
    form_class = PurchaseForm
    success_url = reverse_lazy('sales:purchase_list')
    permission_required = 'change_purchase'

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
    template_name = '/templates/purchase/shopping_cart.html'  # Asegúrate de usar el nombre correcto de tu template
    success_url = reverse_lazy('sales:purchase_list')
    context_object_name = 'purchase'
    permission_required = 'delete_purchase'

    def delete(self, request, *args, **kwargs):
        purchase = self.get_object()
        messages.success(self.request, f"Compra eliminada exitosamente con número de documento {purchase.num_document}.")
        return super().delete(request, *args, **kwargs)


class ProcessPurchaseView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])
            
            for item in cart:
                product_id = item.get('id')
                quantity = item.get('quantity')

                # Asegurarse de que la cantidad es un número entero
                try:
                    quantity = int(quantity)
                except (ValueError, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Cantidad inválida.'}, status=400)
                
                product = get_object_or_404(Product, id=product_id)

                # Asegurarse de que el stock no sea None
                if product.stock is None:
                    product.stock = 0

                product.stock += quantity
                product.save()
            
            return JsonResponse({'status': 'success'}, status=200)
        
        except Exception as e:
            # Registrar el error si es necesario
            print(f'Error: {e}')
            return JsonResponse({'status': 'error', 'message': 'Ocurrió un error al procesar la compra.'}, status=500)
        
class PurchaseHistoryView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'purchase/purchase_history.html'
    model = PurchaseDetail
    context_object_name = 'purchase_details'
    permission_required = 'view_purchase'

    def get_queryset(self):
        return self.model.objects.select_related('purchase', 'product').order_by('-purchase__issue_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial de Compras'
        return context