import formula.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^formula/query/$', formula.apis.query_formula_api, name="formula_query_api"),
]