from django.shortcuts import render, redirect, reverse
from django.contrib import messages

# Create your views here.
from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('items'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JKV7WLy0OFcjMP4BBe1pgGHPEWyvwxKYJuJg7Mnlw9Y8V1I4QfOcodTUIaKubwaRvfJMBqtJXHUJ2aihBzP4aSa0007G5BPVL',
        'client_secret': 'testing_this'
    }

    return render(request, template, context)

