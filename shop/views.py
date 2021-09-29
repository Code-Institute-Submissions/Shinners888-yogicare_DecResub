from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Item
from .forms import itemsForm
from django.contrib.auth.decorators import login_required


def all_items(request):

    items = Item.objects.all()
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


@login_required
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


@login_required
def edit_item(request, item_id):
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = itemsForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully changed item!')
            return redirect(reverse('item_detail', args=[item.id]))
        else:
            messages.error(request, 'Something went wrong, please check information.')
    else:
        form = itemsForm(instance=item)
        messages.info(request, f'You are editing {item.friendly_name}')

    template = 'shop/edit_item.html'
    context = {
        'form': form,
        'item': item,
    }

    return render(request, template, context)


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    messages.success(request, 'Deleted!')
    return redirect(reverse('items'))
