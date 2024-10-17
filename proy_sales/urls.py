from django.conf import settings
from django.conf.urls.static import static
from app.core import views as core
from django.contrib import admin
from django.urls import path, include
from app.core.views.home import HomeTemplateView
from app.core.views.modulos import ModuloTemplateView
from app.core.views.dashboard import ChartTemplateView
urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('',HomeTemplateView.as_view(), name='home'),
    path('modulos/',ModuloTemplateView.as_view(), name='modulos'),
    path('dashboard/',ChartTemplateView.as_view(), name='dashboard'),
    path('security/', include('app.security.urls', namespace='security')),
    path('sales/', include('app.sales.urls', namespace='sales')),
    path('core/', include('app.core.urls', namespace='core')),
    path('purcharse/', include('app.purcharse.urls', namespace='purcharse')),
    # path('signup/', core.signup, name='signup'),
    # path('logout/', core.signout, name='logout'),
    # path('signin/', core.signin, name='signin'),
    # path('profile/', views.profile, name='profile'),
    # path('profile/update/', views.update_profile, name='update_profile'),

    # path('', include('app.core.urls', namespace='core')),
    # path('purchase/', include('app.purchase.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
