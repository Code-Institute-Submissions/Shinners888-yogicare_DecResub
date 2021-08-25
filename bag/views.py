from django.shortcuts import render, redirect
from django.contrib import messages

from shop.models import Item


def shopping_bag(request):

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):

    item = Item.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    colour = None
    if 'item_colour' in request.POST:
        colour = request.POST['item_colour']
    bag = request.session.get('bag', {})

    if colour:
        if item_id in list(bag.keys()):
            if colour in bag[item_id]['items_by_colour'].keys():
                bag[item_id]['items_by_colour'][colour] += quantity
            else:
                bag[item_id]['items_by_colour'][colour] = quantity
        else:
            bag[item_id] = {'items_by_colour': {colour: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {item.name} to your bag')

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


def add_classe_to_bag(request, classe_id):

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if classe_id in list(bag.keys()):
        bag[classe_id] += quantity
    else:
        bag[classe_id] = quantity

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)
