from django.contrib import admin
from .models import Channel,Machine

# Register your models here.


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id','title','remarks')

admin.site.register(Channel,ChannelAdmin)


class MachineAdmin(admin.ModelAdmin):
    list_display = ('id','channel','address','mac_address','password')

admin.site.register(Machine,MachineAdmin)