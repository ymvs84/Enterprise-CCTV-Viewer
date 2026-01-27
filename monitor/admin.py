from django.contrib import admin
from .models import Camara

@admin.register(Camara)
class CamaraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'url_hls', 'activa')