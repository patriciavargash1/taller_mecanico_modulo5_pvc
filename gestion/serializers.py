from rest_framework import serializers
from .models import Cliente, Vehiculo, OrdenReparacion, Mecanico

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    # Mostramos el nombre del dueño en lugar de solo el ID (opcional)
    dueno_detalle = serializers.ReadOnlyField(source='dueno.nombre')

    class Meta:
        model = Vehiculo
        fields = '__all__'

class OrdenReparacionSerializer(serializers.ModelSerializer):
    # Para ver el texto legible del Estado (ej: "En Proceso") en la API
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = OrdenReparacion
        fields = '__all__'
