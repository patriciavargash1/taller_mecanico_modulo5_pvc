from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Cliente, Vehiculo, OrdenReparacion
from .serializers import ClienteSerializer, VehiculoSerializer, OrdenReparacionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
def index(request):
    return HttpResponse("Hola mundo")


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class OrdenReparacionViewSet(viewsets.ModelViewSet):
    # Aquí aplicamos el orden descendente que querías
    queryset = OrdenReparacion.objects.all().order_by('-fecha_ingreso')
    serializer_class = OrdenReparacionSerializer

@api_view(['GET'])
def buscar_vehiculo_placa(request, placa):
    try:
        vehiculo = Vehiculo.objects.get(patente__iexact=placa)     
        serializer = VehiculoSerializer(vehiculo)
        
        return Response({
            "encontrado": True,
            "datos": serializer.data
        }, status=status.HTTP_200_OK)

    except Vehiculo.DoesNotExist:
        return Response({
            "encontrado": False,
            "error": f"No se encontró ningún vehículo con la patente {patente}"
        }, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'nombre', 
            openapi.IN_QUERY, 
            description="Nombre del cliente", 
            type=openapi.TYPE_STRING
        )
    ]
)   
@api_view(['GET'])
def consulta_cliente_completa(request):
    nombre_buscado = request.query_params.get('nombre', None)

    if not nombre_buscado:
        return Response({"error": "Debes proporcionar un nombre para buscar."}, status=400)

    clientes = Cliente.objects.filter(nombre__icontains=nombre_buscado)
    
    if not clientes.exists():
        return Response({"mensaje": "No se encontró ningún cliente con ese nombre."}, status=404)

    resultados = []
    for cliente in clientes:
        # Obtenemos sus vehículos
        vehiculos = Vehiculo.objects.filter(dueno=cliente)
        # Obtenemos sus órdenes que NO estén entregadas
        ordenes = OrdenReparacion.objects.filter(vehiculo__in=vehiculos).exclude(estado='Entregado')
        
        datos_cliente = {
            "cliente": cliente.nombre,
            "telefono": cliente.telefono,
            "vehiculos": [v.patente for v in vehiculos],
            "ordenes_activas": [
                {
                    "id": o.id,
                    "vehiculo": o.vehiculo.patente,
                    "estado": o.get_estado_display(),
                    "costo": o.costo_estimado
                } for o in ordenes
            ]
        }
        resultados.append(datos_cliente)

    return Response(resultados)