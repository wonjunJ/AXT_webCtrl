from django.urls import path
from . import views

app_name = 'AXTctrl'

urlpatterns = [
    path('', views.index, name='index'),
    path('ctrldetail/', views.content, name='status'),
    path('ctrldetail/servoff/', views.motOff, name='off'),
    #path('ctrldetail/estop/', views.movEstop, name='estop'),
    #path('ctrldetail/move/', views.movVel, name='move'),
]