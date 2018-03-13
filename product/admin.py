from django.contrib import admin
from .models import Category,Item,Product

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Category,CategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title','category')
    list_filter = ('category',)


admin.site.register(Item,ItemAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','descp','price','order')


admin.site.register(Product,ProductAdmin)