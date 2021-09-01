from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Classes
from .forms import classeForm


def all_classes(request):

    classes = Classes.objects.all()

    context = {
        'classes': classes,
    }

    return render(request, 'classes/classes.html', context)


def classe_detail(request, classe_id):

    classe = get_object_or_404(Classes, pk=classe_id)

    context = {
        'classe': classe,
    }

    return render(request, 'classes/classe_detail.html', context)


def add_classe(request):
    form = classeForm()
    if request.method == 'POST':
        form = classeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class Added!')
            return redirect(reverse('add_classe'))
        else:
            messages.error(request, 'Oops! Something in your form is incorrect')
    else:
        form = classeForm()

    form = classeForm()
    template = 'classes/add_classe.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
