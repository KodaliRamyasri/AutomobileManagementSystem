from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('contactUs/', views.contactUs, name='contactUs'),
    path('', views.homeView, name=''),

    path('adminClick', views.adminClick, name='adminClick'),
    path('customerClick', views.customerClick, name='customerClick'),
    path('mechanicsClick', views.mechanicsClick, name='mechanicsClick'),

    path('customerSignup', views.customerSignup, name='customerSignup'),
    path('mechanicSignup', views.mechanicSignup, name='mechanicSignup'),
    path('customerLogin', LoginView.as_view(template_name='adminApp/customerLogin.html'), name='customerLogin'),
    path('mechanicLogin', LoginView.as_view(template_name='adminApp/mechanicLogin.html'), name='mechanicLogin'),
    path('adminLogin', LoginView.as_view(template_name='adminApp/adminLogin.html'), name='adminLogin'),

    path('afterLogin', views.afterLogin, name='afterLogin'),
    path('logout', views.logout, name='logout'),

    path('adminDashboard', views.adminDashboard, name='adminDashboard'),

    path('adminCustomer', views.adminCustomer, name='adminCustomer'),
    path('adminViewCustomer', views.adminViewCustomer, name='adminViewCustomer'),
    path('deleteCustomer/<int:pk>', views.deleteCustomer, name='deleteCustomer'),
    path('updateCustomer/<int:pk>', views.updateCustomer, name='updateCustomer'),
    path('adminAddCustomer', views.adminAddCustomer, name='adminAddCustomer'),
    path('adminViewCustomerEnquiry', views.adminViewCustomerEnquiry, name='adminViewCustomerEnquiry'),
    path('adminViewCustomerInvoice', views.adminViewCustomerInvoice, name='adminViewCustomerInvoice'),

    path('adminMechanic', views.adminMechanic,name='adminMechanic'),
    path('adminViewMechanic',views.adminViewMechanic,name='adminViewMechanic'),
    path('adminApproveMechanic', views.adminApproveMechanic, name='adminApproveMechanic'),
    path('approveMechanic/<int:pk>', views.approveMechanic, name='approveMechanic'),
    path('deleteMechanic/<int:pk>', views.deleteMechanic, name='deleteMechanic'),
    path('adminAddMechanic', views.adminAddMechanic, name='adminAddMechanic'),
    path('adminViewMechanic', views.adminViewMechanic, name='adminViewMechanic'),
    path('updateMechanic/<int:pk>', views.updateMechanic, name='updateMechanic'),
    path('adminViewMechanicSalary', views.adminViewMechanicSalary, name='adminViewMechanicSalary'),
    path('updateSalary/<int:pk>', views.updateSalary, name='updateSalary'),
    path('adminMechanicAttendance', views.adminMechanicAttendance,name='adminMechanicAttendance'),
    path('adminTakeAttendance', views.adminTakeAttendance,name='adminTakeAttendance'),
    path('adminViewAttendance', views.adminViewAttendance,name='adminViewAttendance'),

    path('adminRequest', views.adminRequest,name='adminRequest'),
    path('adminViewRequest', views.adminViewRequest, name='adminViewRequest'),
    path('changeStatus/<int:pk>', views.changeStatus, name='changeStatus'),
    path('adminDeleteRequest/<int:pk>', views.adminDeleteRequest, name='adminDeleteRequest'),
    path('adminAddRequest', views.adminAddRequest, name='adminAddRequest'),
    path('adminApproveRequest', views.adminApproveRequest, name='adminApproveRequest'),
    path('approveRequest/<int:pk>', views.approveRequest, name='approveRequest'),
    path('adminViewServiceCost',views.adminViewServiceCost,name='adminViewServiceCost'),
    path('updateCost/<int:pk>', views.updateCost,name='updateCost'),

    path('adminReport', views.adminReport,name='adminReport'),
    path('adminFeedback', views.adminFeedback,name='adminFeedback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)