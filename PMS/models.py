from django.db import models


class Product(models.Model):
    ProId = models.CharField(max_length=100)
    ProName = models.CharField(max_length=100)
    MinLimit = models.IntegerField()
    ComName = models.CharField(max_length=100)
    UCost = models.FloatField()
    RCost = models.FloatField()
    ShelfNo = models.IntegerField()


