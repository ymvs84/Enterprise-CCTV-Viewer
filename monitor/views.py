from django.shortcuts import render
from .models import Camara

def panel_vigilancia(request):
    # Recuperamos de SQL Server todas las cámaras marcadas como activas
    camaras = Camara.objects.filter(activa=True)
    return render(request, 'monitor/panel.html', {'camaras': camaras})