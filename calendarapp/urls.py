from django.urls import path
from .views import holidays_view

urlpatterns = [
    path('holidays/', holidays_view, name='holidays'),
]