from django.db import models


class Item(models.Model):

    class Meta:
        verbose_name_plural = 'Items'

    name = models.CharField(max_length=254, null=True, blank=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    colours = models.BooleanField(default=False, null=True, blank=True)
    if colours:
        black = models.BooleanField(default=False)
        pink = models.BooleanField(default=False)
        yellow = models.BooleanField(default=False)
        red = models.BooleanField(default=False)
        green = models.BooleanField(default=False)
        blue = models.BooleanField(default=False)
    else:
        black = False
        pink = False
        yellow = False
        red = False
        green = False
        blue = False
        

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
