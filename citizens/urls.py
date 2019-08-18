from django.urls import path

from citizens.views import ImportsView

urlpatterns = [
    path('imports/', ImportsView.as_view())
]
