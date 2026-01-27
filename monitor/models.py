from django.db import models


class Camara(models.Model):
    # Opciones para el desplegable de zonas (puedes añadir más)
    ZONAS = [
        ('EXT', 'Exteriores / Parking'),
        ('INT', 'Interiores / Oficinas'),
        ('SEG', 'Seguridad / Accesos'),
        ('OTRO', 'Otras Zonas'),
    ]

    nombre = models.CharField(max_length=100)
    url_hls = models.CharField(max_length=255, help_text="URL del archivo .m3u8 (Ej: http://IP:8888/cam1/index.m3u8)")

    # --- NUEVOS CAMPOS ---
    zona = models.CharField(max_length=5, choices=ZONAS, default='OTRO', verbose_name="Ubicación/Zona")
    activa = models.BooleanField(default=True, verbose_name="¿Cámara Activa?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_zona_display()})"

    class Meta:
        verbose_name = "Cámara de Seguridad"
        verbose_name_plural = "Cámaras de Seguridad"
        ordering = ['zona', 'nombre']  # Ordenar por zona y luego nombre