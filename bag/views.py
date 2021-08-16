from django.shortcuts import render


def shopping_bag(request):

    return render(request, 'bag/bag.html')
