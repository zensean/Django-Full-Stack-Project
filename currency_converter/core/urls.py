from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('rates/', views.rate_list, name='rate_list'),
    path('rates/create/', views.rate_create, name='rate_create'),
    path('rates/update/<int:pk>/', views.rate_update, name='rate_update'),
    path('rates/delete/<int:pk>/', views.rate_delete, name='rate_delete'),
    path('convert/', views.convert_currency, name='convert_currency'),
]
