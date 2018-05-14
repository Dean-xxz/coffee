from django.contrib import admin
from .models import Channel,Machine,Machine_state,Material_state

# Register your models here.


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id','title','mobile','username','is_superuser','remarks')

admin.site.register(Channel,ChannelAdmin)


class MachineAdmin(admin.ModelAdmin):
    list_display = ('id','channel','province','city','address','is_networking','error_state','material_state')
    list_filter = ('is_networking','error_state','material_state')

admin.site.register(Machine,MachineAdmin)

class MachineStateAdmin(admin.ModelAdmin):
    list_display = ('machine','descp','is_cannel')
    list_filter = ('is_cannel',)

admin.site.register(Machine_state,MachineStateAdmin)

class MaterialStateAdmin(admin.ModelAdmin):
    list_display = ('machine','containerid','container','margin')
    list_filter = ('machine',)

admin.site.register(Material_state,MaterialStateAdmin)
