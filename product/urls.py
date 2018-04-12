import product.apis
import product.market_apis
from django.conf.urls import url

urlpatterns = [
    url(r'^product/list/$', product.apis.list_product_api, name="product_list_api"),
    url(r'^item/list/$', product.apis.list_item_api, name="item_list_api"),
    url(r'^market/product/list/$', product.market_apis.list_product_api, name="market_product_list_api"),
    url(r'^market/product_suit/list/$', product.market_apis.list_product_suit_api, name="product_suit_list_api"),

]
