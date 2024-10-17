from django.urls import path
from app.core.views import category, supplier, product, brand, company, line, iva, customer
 
app_name='core' # define un espacio de nombre para la aplicación
urlpatterns = [    
    # URLs de proveedores
    path('supplier_list/', supplier.SupplierListView.as_view() ,name='supplier_list'),
    path('supplier_create/', supplier.SupplierCreateView.as_view(),name='supplier_create'),
    path('supplier_update/<int:pk>/', supplier.SupplierUpdateView.as_view(),name='supplier_update'),
    path('supplier_delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name='supplier_delete'),
    
    path('product_list/', product.ProductListView.as_view(),name='product_list'),
    path('product_create/', product.ProductCreateView.as_view(),name='product_create'),
    path('product_update/<int:pk>/', product.ProductUpdateView.as_view(),name='product_update'),
    path('product_delete/<int:pk>/', product.ProductDeleteView.as_view(),name='product_delete'),
    
    path('brand_list/', brand.BrandListView.as_view(),name='brand_list'),
    path('brand_create/', brand.BrandCreateView.as_view(),name='brand_create'),
    path('brand_update/<int:pk>/', brand.BrandUpdateView.as_view(),name='brand_update'),
    path('brand_delete/<int:pk>/', brand.BrandDeleteView.as_view(),name='brand_delete'),
    
    path('category_list/', category.CategoryListView.as_view(),name='category_list'),
    path('category_create/', category.CategoryCreateView.as_view(),name='category_create'),
    path('category_update/<int:pk>/', category.CategoryUpdateView.as_view(),name='category_update'),
    path('category_delete/<int:pk>/', category.CategoryDeleteView.as_view(),name='category_delete'),

    path('company_list/', company.CompanyListView.as_view(), name='company_list'),
    path('company_create/', company.CompanyCreateView.as_view(), name='company_create'),
    path('company_update/<int:pk>/', company.CompanyUpdateView.as_view(), name='company_update'),
    path('company_delete/<int:pk>/', company.CompanyDeleteView.as_view(), name='company_delete'),

    path('line_list/', line.LineListView.as_view(),name='line_list'),
    path('line_create/', line.LineCreateView.as_view(),name='line_create'),
    path('line_update/<int:pk>/', line.LineUpdateView.as_view(),name='line_update'),
    path('line_delete/<int:pk>/', line.LineDeleteView.as_view(),name='line_delete'),

    path('iva_list/', iva.IvaListView.as_view(),name='iva_list'),
    path('iva_create/', iva.IvaCreateView.as_view(),name='iva_create'),
    path('iva_update/<int:pk>/', iva.IvaUpdateView.as_view(),name='iva_update'),
    path('iva_delete/<int:pk>/', iva.IvaDeleteView.as_view(),name='iva_delete'),    

    path('customer_list/', customer.CustomerListView.as_view(),name='customer_list'),
    path('customer_create/', customer.CustomerCreateView.as_view(),name='customer_create'),
    path('customer_update/<int:pk>/', customer.CustomerUpdateView.as_view(),name='customer_update'),
    path('customer_delete/<int:pk>/', customer.CustomerDeleteView.as_view(),name='customer_delete'),



 ]
    
#     path('purchase/', include('app.purchase.urls')),
# 
