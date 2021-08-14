from django.db import models


class Shop(models.Model):

    class Meta:
        verbose_name_plural = 'Shop'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    price = models.URLField(max_length=1024, null=True, blank=True)
    colours = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
