from django.urls import path
from . import views

app_name = 'proc'

urlpatterns = [
    
    path('', views.Default.as_view(), name='default'),
    path('new/', views.Default.as_view(), name='new'),
    path('format/', views.Formatar.as_view(), name='format'),
]