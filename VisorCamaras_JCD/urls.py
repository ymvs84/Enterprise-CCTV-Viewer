from django.contrib import admin
from django.urls import path
from monitor import views  # Importamos la vista de nuestra app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.panel_vigilancia, name='panel'), # La ruta vacía '' es la home
]