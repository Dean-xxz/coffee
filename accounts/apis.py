#__author__ = "Dean"
#__email__ = "1220543004@qq.com"


"""
此处提供众咖科技微信商城 支付模块所需公共api

"""
import json
import datetime
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from urllib.request import urlopen
from .models import Wechat_user,Invitation,Shopping_cart,Coupon_bank,Notice
from product.models import Product,Item
from access_code.models import Access_Code
from payment.models import Order
from coupon.admin import Coupon
from django.views.generic import View
from .js_utils import get_js_config
from access_code.utils import get_first_access_code
from .oauth import get_access_token,get_userinfo
from django.core.cache import cache
from urllib import parse

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


#授权
class OauthQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
        }

    def access_db(self, kwarg):
        data = {
            "oauth_link":'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxc59b077d6c26e6ff&redirect_uri=http%3a%2f%2fwww.zhongkakeji.com%2fwechat%2foauth&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
        }

        return data

    def format_data(self, data):
        return ok_json(data = data)


query_oauth_api = OauthQueryAPI().wrap_func()

#用户信息查询接口
class UserinfoQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "user_id":'r'
        }

    def access_db(self, kwarg):
        user_id = kwarg['user_id']
        try:
            userinfo = Wechat_user.objects.get(pk=user_id)
            userinfo = userinfo.get_json()
            return userinfo
        except Wechat_user.DoesNotExist:
            return None

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('query faild')


query_userinfo_api = UserinfoQueryAPI().wrap_func()

#js_sdk config 调用config查询
class ConfigQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "url":'r'
        }

    def access_db(self, kwarg):
        url = kwarg['url']
        url = parse.unquote(url)
        data = get_js_config(url=url)
        return data

    def format_data(self, data):
        return ok_json(data = data)


query_config_api = ConfigQueryAPI().wrap_func()



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
            username = user.nickname
            old_bank = Access_Code.objects.get(code = code_id)
            old_user_id = old_bank.user_id
            text = '您赠送给%s的礼物已被领取'%(username)
            notice = Notice(user_id = old_user_id,text = text)
            notice.save()
            bank = Access_Code.objects.filter(code  = code_id).update(user_id = user_id)
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

        bank = Access_Code.objects.filter(user_id = user_id,is_active = True)
        bank = [o.get_json() for o in bank]

        for i in bank:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            item_id = i['item']
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
        return None


    def format_data(self,data):
        return ok_json(data=data)

list_coupon_api = CouponListAPI().wrap_func()

#优惠券领取接口
class MyCouponCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
            'coupon_ids':'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']
        coupon_ids = kwarg['coupon_ids']
        coupon_ids=coupon_ids.replace(',','')
        
        for coupon_id in coupon_ids:
            coupon = Coupon.objects.get(pk = coupon_id)
            dead_line = coupon.dead_line
            try:
                is_recived = Coupon_bank.objects.get(user_id = user_id,coupon_id = coupon_id,is_active = True)
                pass
            except Coupon_bank.DoesNotExist:
                coupon_bank = Coupon_bank(user_id = user_id,coupon_id = coupon_id,dead_line = dead_line)
                coupon_bank.save()
        return 'recived successful'

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
        code = request.GET.get('code')
        if code:
            data = get_access_token(code=code)
            access_token = data['access_token']
            openid = data['openid']
            userinfo = get_userinfo(access_token=access_token,openid=openid)
            nickname = userinfo['nickname']
            openid = userinfo['openid']
            try:
                user = Wechat_user.objects.get(openid = openid)
                data = user.get_json()
                data['user_id'] = data['id']
                user_id = user.id
                print (user_id)
                response = HttpResponseRedirect('/')
                response.set_cookie('user_id',user_id)
                return response
            except Wechat_user.DoesNotExist:
                sex = userinfo['sex']
                language = userinfo['language']
                city = userinfo['city']
                province = userinfo['province']
                country = userinfo['country']
                headimgurl = userinfo['headimgurl']
                wechat_user = Wechat_user(nickname=nickname,openid=openid,sex=sex,language=language,city=city,province=province,country=country,headimgurl=headimgurl)
                wechat_user.save()
                if wechat_user:
                    user_id = wechat_user.id
                    userinfo['user_id'] = user_id
                    create_send_coffee = get_first_access_code(user_id=user_id,item_id=1)
                    response = HttpResponseRedirect('/')
                    response.set_cookie('user_id',user_id)
                    return response
        if not code:
            response = HttpResponseRedirect('/')
            return response



#系统消息查询接口
class NoticeListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "user_id":'r',
        }

    def access_db(self,kwarg):
        user_id = kwarg['user_id']
        notice = Notice.objects.filter(user_id = user_id,is_read = False)
        notice = [o.get_json() for o in notice]
        for i in notice:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            i['notice_id'] = i['id']
            i.pop('id')
        return notice


    def format_data(self,data):
        return ok_json(data=data)

list_notice_api = NoticeListAPI().wrap_func()

#系统消息已读状态更新
class NoticeUpdateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "notice_id":'r',
        }

    def access_db(self,kwarg):
        notice_id = kwarg['notice_id']
        notice = Notice.objects.filter(pk = notice_id).update(is_read = True)
        return 'update successful'


    def format_data(self,data):
        return ok_json(data=data)

update_notice_api = NoticeUpdateAPI().wrap_func()

