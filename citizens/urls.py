from django.urls import path

from citizens.views import ImportsView

app_name = 'citizens'

urlpatterns = [
    path('imports/', ImportsView.as_view(), name='imports')
]
