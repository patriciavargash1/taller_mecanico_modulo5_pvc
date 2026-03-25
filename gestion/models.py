from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Vehiculo(models.Model):
    patente = models.CharField(max_length=15, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(verbose_name="Año")
    # Un vehículo pertenece a un cliente (Relación Uno a Muchos)
    dueno = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="vehiculos")

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"

class Mecanico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"
    
class EstadoOrden(models.TextChoices):
        INGRESADO = 'ING', 'Ingresado'
        EN_PROCESO = 'PRO', 'En Proceso'
        FINALIZADO = 'FIN', 'Finalizado'
        ENTREGADO = 'ENT', 'Entregado'
class OrdenReparacion(models.Model): 
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    mecanico = models.ForeignKey(Mecanico, on_delete=models.SET_NULL, null=True)
    descripcion_falla = models.TextField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=EstadoOrden, default=EstadoOrden.INGRESADO)
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Orden #{self.id} - {self.vehiculo.patente}"
