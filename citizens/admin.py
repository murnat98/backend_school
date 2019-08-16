from django.contrib import admin

from citizens.models import Citizens, Imports, Relatives


@admin.register(Citizens)
class CitizensAdmin(admin.ModelAdmin):
    pass


@admin.register(Imports)
class ImportsAdmin(admin.ModelAdmin):
    pass


@admin.register(Relatives)
class RelativesAdmin(admin.ModelAdmin):
    pass
