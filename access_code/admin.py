from django.contrib import admin
from .models import Access_Code

# Register your models here.


class Access_CodeAdmin(admin.ModelAdmin):
    list_display = ('item','user','code','status')


admin.site.register(Access_Code,Access_CodeAdmin)
