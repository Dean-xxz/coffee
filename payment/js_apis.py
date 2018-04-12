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


# 创建订单接口
class OrderCreationAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'product_id': ('o', None),
            'machine_id': ('o', None),
            'openid':('o', None),
            'total_fee':('o',None),
            'pay_type':('o',None),        #结算方式

        }

    def access_db(self, kwarg):
        product_id = kwarg['product_id']
        channel = kwarg['channel']
        machine_id = kwarg['machine_id']
        openid = kwarg['openid']
        total_fee = kwarg['total_fee']
        channel = 'W'
        # 判断结算方式
        try:
            product = Product.objects.get(pk=product_id)
            body = product.title

            order = Order(product_id=product_id, total_fee=total_fee, channel=channel, machine_id=machine_id)
            order.save()
            out_trade_no = order.id
            # Payment
            total_fee = total_fee * 100
            params = build_form_by_params_js({
                'body': body,
                'out_trade_no': out_trade_no,
                'total_fee': total_fee,
                'spbill_create_ip': '121.201.67.209',
                'openid':openid,
            })
            data = json.dumps(params)
            data = json.loads(data)
            data['out_trade_no'] = out_trade_no
            return data

        except Product.DoesNotExist:
            return None

    def format_data(self, data):
        if data is not None:
            return ok_json(data=data)
        return fail_json('订单创建失败')


create_order_api = OrderCreationAPI().wrap_func()






