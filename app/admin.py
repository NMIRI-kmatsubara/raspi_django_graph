from django.contrib import admin
from .models import Raspi_data
# Register your models here.


class Raspi_dataAdmin(admin.ModelAdmin):
    list_display = ('id', 'data1')
    list_display_links = ('id', 'data1')

admin.site.register(Raspi_data, Raspi_dataAdmin)

