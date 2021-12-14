from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem, weak=False)
def update_on_save(sender, instance, created, **kwargs):

    instance.order.update_total()
    print('signal')
    print('update_on_save')


@receiver(post_delete, sender=OrderLineItem, weak=False)
def update_on_delete(sender, instance, **kwargs):

    instance.order.update_total()
