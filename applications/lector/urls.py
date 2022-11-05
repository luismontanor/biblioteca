from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path(
        'prestamo/add/',
        views.AddPrestamo.as_view(),
        name='prestamo_add'
        ),
    path(
        'prestamo/add-multiple/',
        views.AddMultiplePrestamo.as_view(),
        name='prestamo_add_multiple'
        ),
]