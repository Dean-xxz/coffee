import machine.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^create/$', machine.apis.create_machine_api, name="machine_create_api"),
    url(r'^password/update/$', machine.apis.update_password_api, name="password_update_api"),
    url(r'^log/create/$', machine.apis.create_log_api, name="log_create_api"),
    url(r'^log/delete/$', machine.apis.delete_log_api, name="log_delete_api"),
    url(r'^material/update/$', machine.apis.update_material_api, name="material_update_api"),
    url(r'^channel/login/$', machine.apis.login_mch_api, name="mch_login_api"),
    url(r'^channel/password/update/$', machine.apis.update_mchpsd_api, name="mchpsd_update_api"),
    url(r'^list/mch/$', machine.apis.list_mch_api, name="mch_list_api"),
    url(r'^list/machine/$', machine.apis.list_machine_api, name="machine_list_api"),
]
