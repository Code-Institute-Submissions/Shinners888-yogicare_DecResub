from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_classes, name='classes'),
    path('<classe_id>', views.classe_detail, name='classe_detail'),
]
