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
            'product_ids': 'r',
            # 'user_id':'r',
            # 'openid':('o', None),
            # 'coupon_id':('o',None),
        }

    def access_db(self, kwarg):
        product_ids = kwarg['product_ids']
        print (type(product_ids))
        product_ids=product_ids.replace(',','')
        # openid = kwarg['openid']
        # user_id = kwarg['user_id']
        # coupon_id = kwarg['coupon_id']
        #
        for i in product_ids:
            product = Product.objects.get(pk=i)
            order = Order.objects.get(pk=36)
            order.products.add(product)

            print (i)
        print (product_ids)
        return None
        # total_fee = '12'
        # order = Order(total_fee=total_fee,product_ids=product_ids, channel='W',user_id=user_id,coupon_id=coupon_id,scene='2')
        # order.save()
        # order = order.id
        #
        # return order.get_json()
        # Payment
            #total_fee = total_fee * 100
            #params = build_form_by_params_js({
            #    'body': body,
            #    'out_trade_no': out_trade_no,
            #    'total_fee': total_fee,
            #    'spbill_create_ip': '121.201.67.209',
            #    'openid':openid,
            #})
            #data = json.dumps(params)
            #data = json.loads(data)
            #data['out_trade_no'] = out_trade_no
            #return data

    def format_data(self, data):
        if data is not None:
            return ok_json(data=data)
        return fail_json('订单创建失败')


create_order_api = OrderCreationAPI().wrap_func()






