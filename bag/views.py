from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages

from shop.models import Item


def shopping_bag(request):

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):

    item = get_object_or_404(Item, pk=item_id)
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
                messages.success(request, f'Added {item.friendly_name} to bag')
            else:
                bag[item_id]['items_by_colour'][colour] = quantity
                messages.success(request, f'{item.friendly_name} added to bag')
        else:
            bag[item_id] = {'items_by_colour': {colour: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, 'Added to bag')
        else:
            bag[item_id] = quantity
            messages.success(request, 'Added to bag')

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


def adjust_bag(request, item_id):

    item = get_object_or_404(Item, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    colour = None
    if 'item_colour' in request.POST:
        colour = request.POST['item_colour']
    bag = request.session.get('bag', {})

    if colour:
        if quantity > 0:
            bag[item_id]['items_by_colour'][colour] = quantity
            messages.success(request, f'{item.name} updated in bag')
        else:
            del bag[item_id]['items_by_colour'][colour]
            if not bag[item_id]['items_by_colour']:
                bag.pop(item_id)
            messages.success(request, f'{item.name} updated in bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'{item.name} updated in bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'{item.name} updated in bag')

    request.session['bag'] = bag
    return redirect(reverse('shopping_bag'))


def remove_from_bag(request, item_id):

    try:
        colour = None
        if 'item_colour' in request.POST:
            colour = request.POST['item_colour']
        bag = request.session.get('bag', {})

        if colour:
            del bag[item_id]['items_by_colour'][colour]
            if not bag[item_id]['items_by_colour']:
                bag.pop(item_id)
                messages.success(request, 'Removed from bag')
        else:
            bag.pop(item_id)
            messages.success(request, 'Removed from bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
