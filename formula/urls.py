import formula.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^formula/query/$', formula.apis.query_formula_api, name="formula_query_api"),
    url(r'^container/list/$', formula.apis.list_container_api, name="container_list_api"),

]
