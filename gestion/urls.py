from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, VehiculoViewSet, OrdenReparacionViewSet

# Registramos los ViewSets en el router
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'ordenes', OrdenReparacionViewSet)

urlpatterns = [
               #path('',views.index, name="index"),
               # Esto creará rutas como /api/clientes/, /api/ordenes/, etc.
               path('api/', include(router.urls)),
               path('api/buscar/<str:placa>/', views.buscar_vehiculo_placa, name='buscar-placa'),
               path('api/consulta-taller/', views.consulta_cliente_completa, name='consulta-taller'),
               ]
