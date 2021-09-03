from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Item
from .forms import itemsForm
from django.db.models import Q


def all_items(request):

    items = Item.objects.all()
    query = None
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "What are you looking for?")
                return redirect(reverse('items'))

            queries = Q(name__icontains=query) |\
                Q(description__icontains=query)
            items = items.filter(queries)

    context = {
        'items': items,
    }

    return render(request, 'shop/items.html', context)


def item_detail(request, item_id):

    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item': item,
    }

    return render(request, 'shop/item_detail.html', context)


def add_items(request):
    form = itemsForm()
    if request.method == 'POST':
        form = itemsForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, 'Successfully added item!')
            return redirect(reverse('item_detail', args=[item.id]))
        else:
            messages.error(request, 'Error, please check the info is correct')
    else:
        form = itemsForm()

    template = 'shop/add_items.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    messages.success(request, 'Deleted!')
    return redirect(reverse('items'))
