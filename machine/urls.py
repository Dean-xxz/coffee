import machine.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^create/$', machine.apis.create_machine_api, name="machine_create_api"),
    url(r'^password/update/$', machine.apis.update_password_api, name="password_update_api"),
]