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
    status = models.Choices(
        STATUS_CHOICES,
    )
    
    def calculate_total_price(self):
        pass

    @property
    def total_sum(self):
        return self.calculate_total_price()
    


class OrdersItems(models.Model):

    order = models.ForeignKey(
        Orders,
        related_name='items'
    )
    dish = models.CharField(
        max_length=50,
        verbose_name='Блюдо',
    )
    price = models.PositiveBigIntegerField(
        verbose_name='Цена',
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1,
    )
