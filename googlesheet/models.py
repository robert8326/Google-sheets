from django.db import models


class Receipt(models.Model):
    source_id = models.IntegerField(
        verbose_name='ID объекта в Google sheet',
        blank=True, null=True
    )
    order_id = models.IntegerField(
        verbose_name='ID заказа',
        blank=True, null=True
    )
    price_usd = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True,
        verbose_name='Стоимость в USD'
    )
    price_rub = models.DecimalField(
        max_digits=15, decimal_places=2,
        blank=True, null=True,
        verbose_name='Стоимость в рублях'
    )
    delivery_date = models.DateField(
        verbose_name='Срок поставки',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чек'
