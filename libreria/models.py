from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Empresa(models.Model):
    codigo_empresa = models.CharField(max_length=50, unique=True, verbose_name="Código de Empresa")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    nit = models.CharField(max_length=50, unique=True, verbose_name="NIT")
    direccion = models.CharField(max_length=255, verbose_name="Dirección", null=True, blank=True)
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", null=True, blank=True)
    email = models.EmailField(max_length=100, verbose_name="Email", null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']


# ---------- MANAGER PERSONALIZADO ----------
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nombre, apellido, password, **extra_fields)
    
TIPO_DOCUMENTO_CHOICES = [
    ('CC', 'CC'),
    ('Pasaporte', 'Pasaporte'),
    ('Otro', 'Otro'),
]

# ---------- MODELO USUARIO PERSONALIZADO ----------
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    tipo_documento = models.CharField(
        max_length=20,
        choices=TIPO_DOCUMENTO_CHOICES,
        verbose_name="Tipo de Documento",
        null=True,
        blank=True
    )
    numero_documento = models.CharField(max_length=50, verbose_name="Número de Documento", null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", blank=True)
    descripcion = models.TextField(verbose_name="descripcion", null=True)

    # campos requeridos para AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        super().delete()
