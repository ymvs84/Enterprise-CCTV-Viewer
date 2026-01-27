from django.contrib import admin
from .models import Camara

@admin.register(Camara)
class CamaraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'zona', 'activa', 'url_hls') # Columnas que se ven
    list_filter = ('zona', 'activa') # Filtros laterales
    search_fields = ('nombre',) # Barra de búsqueda
    list_editable = ('activa',) # Activar/Desactivar rápido sin entrar