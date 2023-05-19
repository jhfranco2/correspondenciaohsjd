from django.db import models
from django.forms import ValidationError


#modelo proceso
class Proceso(models.Model):
    nombre_proceso = models.CharField(max_length=32,null=False)

    def __str__(self):
        return self.nombre_proceso 
     
def validate_unique_or_empty(value):
    """
    Valida que el campo sea único cuando no esté vacío.
    """
    if value.strip() != '':
        if Libro.objects.filter(numero_documento=value).exists():
            raise ValidationError('Ya hay un documento con ese número.')
             
# Modelo del libro
class Libro(models.Model):
    sigla = models.CharField(max_length=1,default='C')
    tipo_documento = models.CharField(max_length=1,default='',null=True)
    proveedor = models.CharField(max_length=28,default='')
    numero_documento = models.CharField(
        max_length=48,
        default='',
        null=True,
        blank=True,
        validators=[validate_unique_or_empty]
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    fecha_entrada = models.DateTimeField(auto_now_add=False,blank=False,null=False)
    remitente_destinatario = models.CharField(max_length=1)
    importancia = models.CharField(max_length=1,default='')
    direccion = models.CharField(max_length=48,default='correo electronico',blank=False)
    nombre_destinatario_remitente = models.CharField(max_length=60,default='')
    asunto = models.CharField(max_length=72,default='sin asunto')
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE)
    quien_firma = models.CharField(max_length=48,default='nadie firma')
    quien_solicita_recibe = models.CharField(max_length=48,null=False,blank=False,default='')
    salida = models.DateTimeField(auto_now_add=False,blank=True,null=True,default='')
    registro_de_entrega = models.CharField(max_length=70,default=None,null=True,blank=True)
    observaciones = models.TextField(max_length=120,default='',null=True,blank=True)


    def __str__(self):
        return str(self.id)

# Modelo CI
class Ci(models.Model):
    libro = models.OneToOneField(Libro,models.CASCADE,related_name='ci')

    def __str__(self):
        return str(self.id)
    
# Modelo Z.AND
class Zand(models.Model):
    libro = models.OneToOneField(Libro,models.CASCADE,related_name='zand')

    def __str__(self):
        return str(self.id)    

# Modelo Y.AND
class Gand(models.Model):
    libro = models.OneToOneField(Libro,models.CASCADE,related_name='gand')

    def __str__(self):
        return str(self.id)        