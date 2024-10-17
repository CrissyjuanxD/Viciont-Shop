from django.urls import path
from app.purcharse.views import comprass

app_name = 'purcharse'  # Define un espacio de nombre para la aplicación
urlpatterns = [
    # URLs de compras
    path('purcharse_list/', comprass.PurchaseListView.as_view(), name='purcharse_list'),
    path('purcharse_create/', comprass.PurchaseCreateView.as_view(), name='purcharse_create'),
    path('purcharse_update/<int:pk>/', comprass.PurchaseUpdateView.as_view(), name='purcharse_update'),
    path('purcharse_delete/<int:pk>/', comprass.PurchaseDeleteView.as_view(), name='purcharse_delete'),
    
    path('process_purchase/', comprass.ProcessPurchaseView.as_view(), name='process_purchase'),
    
    path('purchases/history/', comprass.PurchaseHistoryView.as_view(), name='purchase_history'),
]
