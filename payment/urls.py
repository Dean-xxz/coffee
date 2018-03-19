import payment.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^order/create/$', payment.apis.create_order_api, name="order_create_api"),
]