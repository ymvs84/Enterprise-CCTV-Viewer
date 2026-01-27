from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Camara

# --- CONFIGURACIÓN DE LOS BOTONES DE FILTRO ---
# (Código BBDD, Texto en el botón)
MIS_ZONAS = [
    ('EXT', 'Exteriores / Parking'),
    ('INT', 'Interiores / Oficinas'),
    ('SEG', 'Seguridad / Accesos'),
    ('OTRO', 'Otras Zonas'),
]


# VISTA 1: EL DASHBOARD INTELIGENTE 🧠
@login_required
def dashboard(request):
    # CASO A: ES EL ADMIN (SUPERUSUARIO) -> Ve todo + Filtros
    if request.user.is_superuser:
        # 1. Cogemos todas las cámaras activas
        camaras = Camara.objects.filter(activa=True).order_by('id')

        # 2. Aplicamos filtro si han pulsado un botón
        filtro_zona = request.GET.get('zona')  # ¿Han pulsado botón?
        if filtro_zona:
            camaras = camaras.filter(zona=filtro_zona)

        context = {
            'camaras': camaras,
            'titulo_ventana': "PANEL ADMINISTRADOR",
            'zonas': MIS_ZONAS,  # <--- AQUÍ PASAMOS LOS BOTONES
            'filtro_actual': filtro_zona or 'TODAS'
        }
        return render(request, 'monitor/index.html', context)

    # CASO B: ES CONSERJERÍA -> Ve los botones grandes
    else:
        return render(request, 'monitor/dashboard.html')


# VISTA 2: LAS PANTALLAS DIVIDIDAS (CONSERJERÍA)
@login_required
def monitor_screen(request, pantalla_id):
    todas = Camara.objects.filter(activa=True).order_by('id')

    if pantalla_id == 1:
        camaras_mostrar = todas[:6]
        titulo = "MONITOR 1 (Izquierdo)"
    elif pantalla_id == 2:
        camaras_mostrar = todas[6:12]
        titulo = "MONITOR 2 (Derecho)"
    else:
        camaras_mostrar = todas
        titulo = "VISOR"

    context = {
        'camaras': camaras_mostrar,
        'titulo_ventana': titulo,
        'zonas': [],
        'filtro_actual': 'TODAS'
    }
    return render(request, 'monitor/index.html', context)