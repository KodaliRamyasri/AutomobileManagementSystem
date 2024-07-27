from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('customerDashboard', views.customerDashboard, name='customerDashboard'),
    path('customerRequest', views.customerRequest, name='customerRequest'),
    path('customerAddRequest', views.customerAddRequest, name='customerAddRequest'),
    path('customerProfile', views.customerProfile, name='customerProfile'),
    path('editCustomerProfile', views.editCustomerProfile, name='editCustomerProfile'),
    path('customerFeedback', views.customerFeedback, name='customerFeedback'),
    path('customerInvoice', views.customerInvoice, name='customerInvoice'),
    path('customerViewRequest', views.customerViewRequest, name='customerViewRequest'),
    path('customerDeleteRequest/<int:pk>', views.customerDeleteRequest, name='customerDeleteRequest'),
    path('customerViewApprovedRequest', views.customerViewApprovedRequest,
         name='customerViewApprovedRequest'),
    path('customerViewApprovedRequestInvoice', views.customerViewApprovedRequestInvoice,
         name='customerViewApprovedRequestInvoice'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)