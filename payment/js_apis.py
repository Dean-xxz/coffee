# __author__ = "Dean"
# __email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 支付模块所需公共api
"""
import json
from utils.view_tools import ok_json, fail_json
from utils.abstract_api import AbstractAPI

from .models import Order
from product.models import Product
from .js_wechat_pay import build_form_by_params_js
from accounts.models import Wechat_user

# 创建订单接口
class OrderCreationAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'product_ids': 'r',
            'user_id':'r',
            'coupon_id':('o',None),
        }

    def access_db(self, kwarg):
        product_ids = kwarg['product_ids']
        product_ids=product_ids.replace(',','')
        user_id = kwarg['user_id']
        coupon_id = kwarg['coupon_id']
        wechat_user = Wechat_user.objects.get(pk=user_id)
        openid = wechat_user.openid

        order = Order(total_fee = 12,coupon_bank_id = coupon_id,user_id = user_id,channel = 'W')
        order.save()
        for i in product_ids:
            product = Product.objects.get(pk=i)
            order.products.add(product)

        # Payment
        total_fee = 1
        body = 'test'
        out_trade_no = order.id
        openid = openid
        params = build_form_by_params_js({
            'body': body,
            'out_trade_no': out_trade_no,
            'total_fee': total_fee,
            'spbill_create_ip': '121.201.67.209',
            'openid':openid,
            })
#        data = json.dumps(params)
#        data = json.loads(data)
        params['timestamp']=params['timeStamp']
        params.pop('timeStamp')
        return params

    def format_data(self, data):
        if data is not None:
            return ok_json(data=data)
        return fail_json('订单创建失败')


create_order_api = OrderCreationAPI().wrap_func()






