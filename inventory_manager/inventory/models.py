from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F

# Modelo principal: Producto (Capa de acceso a datos)
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# Modelo secundario: Movimientos de inventario
class Movement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def stock_delta(self):
        """Cantidad que este movimiento agrega (o resta) al inventario."""
        return self.quantity if self.movement_type == 'IN' else -self.quantity

    def clean(self):
        """Evita registrar salidas que dejen el inventario bajo cero."""
        if not self.product_id:
            return

        available_stock = self.product.stock
        if self.pk:
            previous = Movement.objects.get(pk=self.pk)
            if previous.product_id == self.product_id:
                available_stock -= previous.stock_delta

        if available_stock + self.stock_delta < 0:
            raise ValidationError({'quantity': 'La salida no puede dejar el stock en negativo.'})

    def save(self, *args, **kwargs):
        """Persiste el movimiento y sincroniza el stock usando el ORM."""
        with transaction.atomic():
            previous = Movement.objects.filter(pk=self.pk).first() if self.pk else None
            if previous:
                Product.objects.filter(pk=previous.product_id).update(
                    stock=F('stock') - previous.stock_delta
                )
            Product.objects.filter(pk=self.product_id).update(
                stock=F('stock') + self.stock_delta
            )
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Al borrar, revierte el efecto del movimiento en el stock."""
        with transaction.atomic():
            Product.objects.filter(pk=self.product_id).update(stock=F('stock') - self.stock_delta)
            return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.movement_type}"

    class Meta:
        ordering = ['-created_at']
