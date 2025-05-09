from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dynamic-tables/', views.dynamic_tables, name='dynamic_dt'),
    path('dynamic-api/', views.dynamic_api, name='dynamic_api'),
    path('charts/', views.charts, name='charts'),
    path('tables/', views.tables, name='tables'),
    path('billing/', views.billing, name='billing'),
    path('virtual-reality/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('profile/', views.profile, name='profile'),
    
    # Authentication
    #path('login/', views.CustomLoginView.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    #path('register/', views.register, name='register'),
]