from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Item


def bag_contents(request):

    bag_items = []
    total = 0
    item_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_info in bag.items():
        if isinstance(item_info, int):
            item = get_object_or_404(Item, pk=item_id)
            total += item_info * item.price
            item_count += item_info
            bag_items.append({
                'item_id': item_id,
                'quantity': item_info,
                'item': item,
            })
        else:
            item = get_object_or_404(Item, pk=item_id)
            for colour, quantity in item_info['items_by_colour'].items():
                total += quantity * item.price
                item_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_info,
                    'item': item,
                    'colour': colour,
                })
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': item_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
