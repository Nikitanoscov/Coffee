from django.db import models


class Orders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.PositiveSmallIntegerField(
        verbose_name='Номер стола'
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20
    )

    @property
    def total_price(self):
        """
        Динамическое вычисление общей стоимости заказа.
        Учитываются цены и количество всех блюд, связанных с заказом.
        """
        return sum(item.price * item.quantity for item in self.items.all())


class OrdersItems(models.Model):

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
        verbose_name='Цена'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1,
    )
