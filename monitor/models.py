from django.db import models

class Camara(models.Model):
    nombre = models.CharField(max_length=100, help_text="Ej: Entrada Principal")
    url_hls = models.CharField(max_length=200, help_text="La URL http://...m3u8")
    activa = models.BooleanField(default=True, help_text="Desmarcar para ocultar esta cámara")

    def __str__(self):
        return self.nombre