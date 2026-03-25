from django.contrib import admin

from .models import Cliente, Vehiculo, Mecanico, OrdenReparacion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'dueno')

@admin.register(Mecanico)
class MecanicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad', 'activo')

@admin.register(OrdenReparacion)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'estado', 'fecha_ingreso')
    list_filter = ('estado', 'mecanico') # Filtros laterales muy útiles
    ordering = ('-fecha_ingreso',)
    search_fields = ('vehiculo',)
