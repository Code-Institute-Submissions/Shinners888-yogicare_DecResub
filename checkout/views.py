from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItems
from shop.models import Item
from bag.contexts import bag_contents

import stripe
import json


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_info in bag.items():
                try:
                    item = Item.objects.get(id=item_id)
                    if isinstance(item_info, int):
                        order_line_item = OrderLineItems(
                            order=order,
                            item=item,
                            quantity=item_info,
                        )
                        order_line_item.save()
                    else:
                        for colour, quantity in item_info['items_by_colour'].items():
                            order_line_item = OrderLineItems(
                                order=order,
                                item=item,
                                quantity=quantity,
                                item_colour=colour,
                            )
                            order_line_item.save()
                except Item.DoesNotExist:
                    messages.error(request, (
                        f'We are out of stock of {self.item.friendly_name} '
                        'Please call us for assistance!')
                    )
                    order.delete()
                    return redirect(reverse('shopping_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_successful',
                                    args=[order.order_number]))
        else:
            messages.error(request, 'There appears to be an error in your info. \
                Please double check. Hint: Use country code instead of name')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "Your bag is empty")
            return redirect(reverse('items'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Check Env')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_successful(request, order_number):
    # save info and successful checkout handler
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, "Order successfully processed!")

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_successful.html'
    context = {
        'order': order,
    }

    return render(request, template, context)