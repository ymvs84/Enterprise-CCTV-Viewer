from django.core.management.base import BaseCommand
from monitor.models import Camara


class Command(BaseCommand):
    help = 'Carga el inventario REAL de JCDecaux conectando con MediaMTX'

    def handle(self, *args, **kwargs):
        # 1. LIMPIEZA
        self.stdout.write("Borrando configuracion anterior...")
        Camara.objects.all().delete()

        # DIRECCIÓN DEL SERVIDOR MEDIAMTX (Local)
        # Puerto 8888 es el estándar para HLS en MediaMTX
        BASE_STREAM_URL = "http://127.0.0.1:8888"

        # 2. DEFINICIÓN DE CÁMARAS
        # Formato: (Nombre Web, Zona, ID_en_MediaMTX)
        datos_camaras = [
            # --- IPRONET ---
            ("Parking Dirección", "EXT", "ipronet_parking_dir"),
            ("Parking Flota", "EXT", "ipronet_parking_flota"),
            ("Entrada Empleados 1", "SEG", "ipronet_entrada_empl"),
            ("Patio Exterior Piscina", "OTRO", "ipronet_patio_piscina"),
            ("Entrada Cartelería", "INT", "ipronet_carteleria"),
            ("Entrada Principal", "SEG", "ipronet_entrada_ppal"),

            # --- AXIS ---
            ("Parking Cartelería", "EXT", "axis_parking_cart"),
            ("Esquina Edificio", "EXT", "axis_esquina"),
            ("Parking Empleados Ext.", "EXT", "axis_parking_ext"),
            ("Patio Lámina Agua", "OTRO", "axis_patio_agua"),
            ("CPD (Centro de Datos)", "SEG", "axis_cpd"),
            ("Puerta Blanca", "SEG", "axis_puerta_blanca"),
            ("Patio Interior Peq.", "INT", "axis_patio_int"),
        ]

        # 3. CREACIÓN EN BBDD
        self.stdout.write("Conectando camaras al sistema...")

        for nombre_web, zona, id_mtx in datos_camaras:
            # Construimos la URL final: http://IP:8888/nombre_camara/index.m3u8
            url_final = f"{BASE_STREAM_URL}/{id_mtx}/index.m3u8"

            Camara.objects.create(
                nombre=nombre_web,
                zona=zona,
                url_hls=url_final,
                activa=True
            )
            self.stdout.write(self.style.SUCCESS(f'   Enlazada: {nombre_web} -> {id_mtx}'))

        self.stdout.write(self.style.SUCCESS('--- SISTEMA EN LINEA: CONFIGURACION REAL APLICADA ---'))