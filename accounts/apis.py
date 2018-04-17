#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技微信商城 支付模块所需公共api
"""
import datetime
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Wechat_user,Invitation,Shopping_cart,Coffee_bank,Coupon_bank
from product.models import Product,Item
from access_code.models import Access_Code
from payment.models import Order
from coupon.admin import Coupon
# 微信新用户注册
class UserCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'openid':'r',
            'nickname':'r',
            'sex':'r',
            'headimgurl': 'r',
            'province':('o',None),
            'city':('o',None),
            'country':('o',None),
            'language':('o',None),
            'privilege':('o',None),
        }

    def access_db(self, kwarg):
        openid = kwarg['openid']
        nickname = kwarg['nickname']
        sex = kwarg['sex']
        province = kwarg['province']
        city = kwarg['city']
        country = kwarg['country']
        headimgurl = kwarg['headimgurl']
        language = kwarg['language']
        privilege = kwarg['privilege']


        try:
            user = Wechat_user.objects.get(openid = openid)
            data = user.get_json()
            return data
        except Wechat_user.DoesNotExist:
            wechat_user = Wechat_user(openid=openid, nickname=nickname,sex=sex,city=city,
                                      province=province,country=country, headimgurl=headimgurl,
                                      language=language,privilege=privilege)
            wechat_user.save()
            if wechat_user:
                data = wechat_user.get_json()
                return data

            return 'create faild!'

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)


create_user_api = UserCreateAPI().wrap_func()


#微信授权code换取openid
class OpenidQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'code':'r',
        }

    def access_db(self, kwarg):
        code = kwarg['code']
        Appid = 'wx2ef73a7f200e1409'
        AppSecret = 'acb9a3a794fa80effbd3e370f65f555f'
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code"%(Appid,AppSecret,code)
        res = urlopen(url).read().decode("utf8")
        message = json.loads(res)
        data = message

        return data

    def format_data(self, data):
        return ok_json(data = data)


query_openid_api = OpenidQueryAPI().wrap_func()

#添加购物车商品
class CartCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
            'product_id':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']
        product_id = kwarg['product_id']
        
        try:
            user = Wechat_user.objects.get(pk = user_id)
            cart = Shopping_cart(user_id = user_id,product_id = product_id)
            cart.save()
            if cart:
                data = 'add cart successful'
                return data
            else:
                return None
        except Wechat_user.DoesNotExist:
            return None

    def format_data(self,data):
        if data is not None:
            return ok_json(data=data)
        return fail_json('add cart faild')

create_cart_api = CartCreateAPI().wrap_func()



#购物车商品删除接口
class CartDeleteAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
            'product_id':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']
        product_id = kwarg['product_id']
        cart = Shopping_cart.objects.filter(user_id = user_id,product_id = product_id).update(is_active = False)
        data = 'delete successful'
        return data

    def format_data(self,data):
        return ok_json(data=data)

delete_cart_api = CartDeleteAPI().wrap_func()


#购物车列表查询接口
class CartListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']

        cart = Shopping_cart.objects.filter(user_id = user_id,is_active = True)
        cart = [o.get_json() for o in cart]

        for i in cart:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            product_id = i['product']
            product_info = Product.objects.get(pk = product_id)
            product_info = product_info.get_json()
            i['product_info'] = product_info

        return cart
            

    def format_data(self,data):
        return ok_json(data=data)

list_cart_api = CartListAPI().wrap_func()


#添加到我的咖啡库接口
class BankCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
            'code_id':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']
        code_id = kwarg['code_id']

        try:
            user = Wechat_user.objects.get(pk = user_id)
            try:
                bank = Coffee_bank.objects.get(user_id = user_id,access_code_id = code_id)
                return 'add coffee_bank successful'
            except Coffee_bank.DoesNotExist:
                bank = Coffee_bank(user_id = user_id,access_code_id = code_id)
                bank.save()
                if bank:
                    data = 'add coffee_bank successful'
                    return data
                else:
                    return None
        except Wechat_user.DoesNotExist:
            return None

    def format_data(self,data):
        if data is not None:
            return ok_json(data=data)
        return fail_json('add coffee_bank faild')

create_bank_api = BankCreateAPI().wrap_func()


#咖啡库中咖啡赠送
class BankUpdateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
            'code_id':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']
        code_id = kwarg['code_id']

        try:
            user = Wechat_user.objects.get(pk = user_id)
            bank = Coffee_bank.objects.filter(access_code_id = code_id).update(user_id = user_id)
            return 'update coffee_bank success'
        except Wechat_user.DoesNotExist:
            return None

    def format_data(self,data):
        if data is not None:
            return ok_json(data=data)
        return fail_json('update coffee_bank faild')

update_bank_api = BankUpdateAPI().wrap_func()


#我的咖啡库列表查询接口
class BankListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']

        bank = Coffee_bank.objects.filter(user_id = user_id,is_active = True)
        bank = [o.get_json() for o in bank]

        for i in bank:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            code_id = i['access_code']
            code = Access_Code.objects.get(pk = code_id)
            code = code.get_json()
            item_id = code['item']
            item = Item.objects.get(pk = item_id)
            item = item.get_json()
            i['item_info'] = item

        return bank


    def format_data(self,data):
        return ok_json(data=data)

list_bank_api = BankListAPI().wrap_func()


#我的订单列表
class OrderListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']

        order = Order.objects.filter(user_id = user_id,is_active = True,is_payment = True)
        order = [o.get_json() for o in order]

        for i in order:
            product_ids = i['products']
            i['product_info'] = []
            for j in product_ids:
                product_info = Product.objects.get(pk = j)
                product_info = product_info.get_json()
                i['product_info'].append(product_info)

        return order


    def format_data(self,data):
        return ok_json(data=data)

list_order_api = OrderListAPI().wrap_func()


#优惠券列表接口
class CouponListAPI(AbstractAPI):
    def config_args(self):
        self.args = {

        }

    def access_db(self,kwarg):

        coupon = Coupon.objects.filter(dead_line__gt=datetime.datetime.now().date(), is_active=True)
        coupon = [o.get_json() for o in coupon]
        for i in coupon:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
        return coupon


    def format_data(self,data):
        return ok_json(data=data)

list_coupon_api = CouponListAPI().wrap_func()

#优惠券领取接口
class MyCouponCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
            'coupon_id':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']
        coupon_id = kwarg['coupon_id']

        try:
            coupon = Coupon.objects.get(pk = coupon_id)
            dead_line = coupon.dead_line
            try:
                is_recived = Coupon_bank.objects.get(user_id = user_id,coupon_id = coupon_id,is_active = True)
                return 'recive successful'
            except Coupon_bank.DoesNotExist:
                coupon_bank = Coupon_bank(user_id = user_id,coupon_id = coupon_id,dead_line = dead_line)
                coupon_bank.save()
                if coupon:
                    data = 'recive successful'
                    return data
                return None
        except Coupon.DoesNotExist:
            return None


    def format_data(self,data):
        if data is not None:
            return ok_json(data=data)
        return fail_json('recive faild')

create_mycoupon_api = MyCouponCreateAPI().wrap_func()


#我的优惠券列表接口
class MyCouponListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']

        coupon = Coupon_bank.objects.filter(dead_line__gt=datetime.datetime.now().date(), is_active=True,user_id=user_id)
        coupon = [o.get_json() for o in coupon]
        for i in coupon:
            coupon_id = i['coupon']
            coupon_info = Coupon.objects.get(pk=coupon_id)
            coupon_info = coupon_info.get_json()
            coupon_info.pop('create_time')
            coupon_info.pop('update_time')
            coupon_info.pop('is_active')
            i['coupon_info'] = coupon_info
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
        return coupon


    def format_data(self,data):
        return ok_json(data=data)

list_mycoupon_api = MyCouponListAPI().wrap_func()


class CodeView(View):
    def get(self, request, *args, **kwargs):
            #get password and username
        code = request.GET.get('code')
        data = code
        print (data)
            #如果不成功，测取消订单
        return None