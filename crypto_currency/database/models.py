from django.db import models


class CryptocurrencyPrices(models.Model):
    datatime = models.DateTimeField(auto_now_add=True)
    cryptocurrency_name = models.TextField(max_length=6)
    price = models.FloatField()

    def __str__(self):
        return self.cryptocurrency_name
