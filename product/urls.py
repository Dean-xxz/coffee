import product.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^product/list/$', product.apis.list_product_api, name="product_list_api"),
]