#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技微信商城 支付模块所需公共api
"""

from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Wechat_user,Invitation



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