from django.contrib import admin
from .models import Formula,Container

# Register your models here.

class ContainerAdmin(admin.ModelAdmin):
    list_display = ('title','size','order','remarks')


admin.site.register(Container,ContainerAdmin)


class FormulaAdmin(admin.ModelAdmin):
    list_display = ('item','container','consumption','water','order','remarks')
    list_filter = ('item',)


admin.site.register(Formula,FormulaAdmin)

