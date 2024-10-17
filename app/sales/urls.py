from django.urls import path
from app.sales.views import sale
from app.purcharse.views.comprass import PurchaseHistoryView
from app.sales.views import sale
from app.sales.views.estadistica import estadisticas_venta
 
app_name='sales' # define un espacio de nombre para la aplicación
urlpatterns = [    
    # URLs de proveedores
    path('sales_list/', sale.SaleListView.as_view() ,name='sales_list'),
    path('sales_create/', sale.SaleCreateView.as_view(),name='sales_create'),
    path('sales_update/<int:pk>/', sale.SaleUpdateView.as_view(),name='sales_update'),
    path('sales_delete/<int:pk>/', sale.SaleDeleteView.as_view(),name='sales_delete'),
    path('sales/graph/', sale.SalesGraphView.as_view(), name='sales_graph'),
    path('anular/<int:invoice_id>/', sale.AnularFacturaView.as_view(), name='anular_factura'),
    path('invoice/<int:invoice_id>/pdf/', sale.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('history/', PurchaseHistoryView.as_view(), name='purchase_history'),
    path('estadisticas_venta/', estadisticas_venta, name='estadisticas_venta'),
 ]