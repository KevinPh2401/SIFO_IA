from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")  # Campo obligatorio
    apellido = models.CharField(max_length=100, verbose_name="Apellido")  # Campo obligatorio
    email = models.EmailField(max_length=100, verbose_name="Email", unique=True)
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    tipo_documento = models.CharField(max_length=50, verbose_name="Tipo de Documento", null=True, blank=True)
    numero_documento = models.CharField(max_length=50, verbose_name="Número de Documento", null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", blank=True)
    descripcion = models.TextField(verbose_name="descripcion", null=True)


    def __str__(self):
        fila = "Nombre: " + self.nombre + " Apellido: " + self.apellido + " - " + "Email: " + self.email + " - " + "Telefono: " + self.telefono + " - " + "Fecha de Nacimiento: " + str(self.fecha_nacimiento) + " - " + "Tipo de Documento: " + self.tipo_documento + " - " + "Numero de Documento: " + self.numero_documento + " - " + "Descripcion: " + self.descripcion
        return fila
   
    def delete(self, using=None, keep_parents=False):
        # Eliminar la imagen del sistema de archivos
            self.imagen.storage.delete(self.imagen.name)
            super().delete()