from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('user_panel/', views.user_panel, name='user_panel'),
    path('search/', views.search, name='search'),  # Маршрут для поиска
    path('praktika/<int:pk>/', views.praktika_detail, name='praktika_detail'),
]