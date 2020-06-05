from django.db import models


# Product
class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)

    def __str__(self):
        return self.name


# Offer
class Offer(models.Model):
    code = models.CharField(max_length=7)
    description = models.CharField(max_length=225)
    discount = models.FloatField()

    def __str__(self):
        return self.code
