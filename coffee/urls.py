from django.contrib import admin
from django.conf.urls import url,include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ad/', include('ad.urls', namespace="ad")),   # 广告模块接口url
    url(r'^product/', include('product.urls', namespace="product")),  # 产品模块接口url
    # url(r'^payment/', include('payment.urls', namespace="payment")),  # 支付模块接口url
    url(r'^formula/', include('formula.urls', namespace="formula")),  # 配方模块接口url
    url(r'^code/', include('access_code.urls', namespace="code")),  # 取货模块接口url

]
