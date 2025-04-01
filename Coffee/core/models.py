from django.core.validators import MinValueValidator
from django.db import models


class Orders(models.Model):
    """
    Класс заказов.
    """
    STATUS_CHOICES = [
        ('В ожидании', 'В ожидании'),
        ('Готово', 'Готово'),
        ('Оплачено', 'Оплачено'),
    ]

    table_number = models.PositiveSmallIntegerField(
        verbose_name='Номер стола'
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20,
        default='В ожидании'
    )

    @property
    def total_price(self):
        """
        Динамическое вычисление общей стоимости заказа.
        Учитываются цены и количество всех блюд, связанных с заказом.
        """
        return sum(item.price * item.quantity for item in self.items.all())


class OrdersItems(models.Model):
    """
    Класс для связывания закозов с блюдами.
    """

    order = models.ForeignKey(
        Orders,
        related_name='items',
        on_delete=models.CASCADE
    )
    dish = models.CharField(
        max_length=50,
        verbose_name='Блюдо',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        validators=[MinValueValidator(1)]
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1,
        validators=[MinValueValidator(1)]
    )
