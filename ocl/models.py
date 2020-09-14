from django.db import models

# Create your models here.


class Tipo(models.Model):

    descripcion = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Tipo de Material'
        verbose_name_plural = 'Tipo de Materiales'

    def __str__(self):
        return self.descripcion


class Almacen(models.Model):

    largo = models.IntegerField()
    cantidad = models.IntegerField()
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Almacen'
        verbose_name_plural = 'Almacenes'

    def __str__(self):
        return str(self.largo)


class Formato(models.Model):

    formato = models.IntegerField()
    perdida = models.IntegerField()

    class Meta:
        verbose_name = 'Formato'
        verbose_name_plural = 'Formatos'

    def __str__(self):
        return str(self.formato)


