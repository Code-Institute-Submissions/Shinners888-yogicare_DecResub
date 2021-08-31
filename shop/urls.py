from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_items, name='items'),
    path('<item_id>', views.item_detail, name='item_detail'),
    path('add/', views.add_items, name='add_items'),
]
