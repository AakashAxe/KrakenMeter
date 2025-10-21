from django.urls import path

from . import views

urlpatterns = [
    path('read/<str:path>', views.read, name='read'),
]
