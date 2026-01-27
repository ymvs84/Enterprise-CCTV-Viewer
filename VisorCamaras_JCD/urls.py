from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from monitor import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. LOGIN
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # 2. LOGOUT
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 3. EL DASHBOARD
    path('', views.dashboard, name='dashboard'),

    # 4. PANTALLAS (Monitor 1 o 2)
    path('monitor/<int:pantalla_id>/', views.monitor_screen, name='monitor_screen'),
]