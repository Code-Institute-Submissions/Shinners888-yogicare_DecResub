import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from shop.models import Item
from profiles.models import yogiUser


class Order(models.Model):
    user_profile = models.ForeignKey(yogiUser, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10,
                                      decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10,
                                      decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def update_total(self):
        SDP = settings.STANDARD_DELIVERY_PERCENTAGE / 100
        self.order_total = self.orderlines.aggregate(
                           Sum('orderline_total'))['orderline_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * SDP
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItems(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='orderlines')
    item = models.ForeignKey(Item, null=False, blank=False,
                             on_delete=models.CASCADE)
    item_colour = models.CharField(max_length=2, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    orderline_total = models.DecimalField(max_digits=6,
                                          decimal_places=2, null=False,
                                          blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.orderline_total = self.item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'You have {self.item.friendly_name} '
        'on order {self.order.order_number}'
