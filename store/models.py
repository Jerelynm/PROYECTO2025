#from django.db import models   ---- globaliza
from django.db import models
from django.utils.text import slugify


# Nota pedagógica:
# - "models.Model" indica que esta clase se convertirá en una TABLA de la BD.
# - Un "campo" (CharField, DecimalField, etc.) es una COLUMNA en esa tabla.
# - "__str__" define cómo se verá el objeto al imprimirlo (útil en el admin).


class TimeStampedModel(models.Model):
    """
    Mixin reutilizable: agrega columnas de auditoría a cualquier tabla que herede de esto.
    No se crea tabla para esta clase porque "abstract = True".
    """
    created_at = models.DateTimeField(auto_now_add=True)  # Se setea al crear
    updated_at = models.DateTimeField(auto_now=True)      # Se actualiza en cada guardado

    class Meta:
        abstract = True  # No crear tabla para este mixin


class Category(TimeStampedModel):
    """
    Agrupa productos: 'Laptops', 'Móviles', 'Accesorios', etc.
    """
    name = models.CharField(max_length=100, unique=True)  # Nombre visible
    slug = models.SlugField(max_length=120, unique=True)  # Para URL amigable (/laptops/)

    class Meta:
        ordering = ['name']  # Orden alfabético por defecto en consultas
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name


class Brand(TimeStampedModel):
    """
    Marca del producto: 'Apple', 'Samsung', 'Lenovo', etc.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """
    Entidad central: lo que vendemos. Mantenerla simple para iniciar.
    """
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)

    # DecimalField = dinero sin errores de flotantes.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # hasta 99,999,999.99
    stock = models.PositiveIntegerField(default=0)                # existencias (no negativos)
    is_active = models.BooleanField(default=True)                 # visible/oculto en catálogo

    class Meta:
        indexes = [
            models.Index(fields=['slug']),         # Búsquedas rápidas por slug
            models.Index(fields=['is_active']),    # Filtros por disponibilidad
        ]
        ordering = ['name']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        # Lo que ves en el admin y consola
        return f'{self.name} ({self.brand})'


class ContactMessage(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    subject = models.CharField(max_length=120)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} — {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    # FK a Category. Marcamos null/blank para migrar sin pedir valor por consola.
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products",
        null=True, blank=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   # <- importante

    @property
    def on_sale(self):
        return self.discount_price is not None and self.discount_price < self.price

    @property
    def final_price(self):
        return self.discount_price if self.on_sale else self.price



    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:120]
            candidate = base
            i = 2
            while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{i}"
                i += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    @property
    def on_sale(self):
        return self.discount_price is not None and self.discount_price < self.price

    @property
    def final_price(self):
        return self.discount_price if self.on_sale else self.price

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=120, blank=True, default="")
    customer_email = models.EmailField(blank=True, default="")
    shipping_address = models.CharField(max_length=250, blank=True, default="")
    items = models.JSONField(default=list)  # snapshot del carrito
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} — {self.created_at:%Y-%m-%d %H:%M}"