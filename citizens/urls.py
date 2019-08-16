from django.urls import path

from citizens.views import Imports

urlpatterns = [
    path('imports/', Imports.as_view())
]
