from django.urls import path

from citizens.views import ImportsView, ChangeImports, CitizensList, CitizenBirthdaysStat, \
    CitizensTownsStatPercentileAge

app_name = 'citizens'

urlpatterns = [
    path('imports/', ImportsView.as_view(), name='imports'),
    path('imports/<int:import_id>/citizens/<int:citizen_id>/', ChangeImports.as_view(), name='change_imports'),
    path('imports/<int:import_id>/citizens/', CitizensList.as_view(), name='list'),
    path('imports/<int:import_id>/citizens/birthdays/', CitizenBirthdaysStat.as_view(), name='birthdays'),
    path('imports/<int:import_id>/towns/stat/percentile/age/', CitizensTownsStatPercentileAge.as_view(),
         name='towns_stat_percentile_age'),
]
