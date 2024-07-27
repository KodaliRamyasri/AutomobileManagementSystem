from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('mechanicDashboard', views.mechanicDashboard, name='mechanicDashboard'),
    path('mechanicWorkAssigned', views.mechanicWorkAssigned, name='mechanicWorkAssigned'),
    path('mechanicUpdateStatus/<int:pk>', views.mechanicUpdateStatus, name='mechanicUpdateStatus'),
    path('mechanicFeedback', views.mechanicFeedback, name='mechanicFeedback'),
    path('mechanicSalary', views.mechanicSalary, name='mechanicSalary'),
    path('mechanicProfile', views.mechanicProfile, name='mechanicProfile'),
    path('editMechanicProfile', views.editMechanicProfile, name='editMechanicProfile'),
    path('mechanicAttendance', views.mechanicAttendance, name='mechanicAttendance'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)