from django.urls import path

from citizens.views import ImportsView, ChangeImports

app_name = 'citizens'

urlpatterns = [
    path('imports/', ImportsView.as_view(), name='imports'),
    path('imports/<int:import_id>/citizens/<int:citizen_id>/', ChangeImports.as_view(), name='change_imports'),
]
