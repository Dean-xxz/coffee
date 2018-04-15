#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 广告模块所需公共api
"""

from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Advertisement,Preference

# 广告列表接口


class AdListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "is_terminal":('o',None)
        }

    def access_db(self, kwarg):
        is_terminal = kwarg['is_terminal']
        print (is_terminal)
        if is_terminal == 'False':
            ad_list = Advertisement.objects.filter(is_active=True,is_terminal=False)
            data = [o.get_json() for o in ad_list]
            for i in data:
                preference = Preference.objects.get(pk=1)
                i['preference'] = preference.title
                i.pop('is_active')
                i.pop('update_time')
                i.pop('create_time')
            return data
        ad_list = Advertisement.objects.filter(is_active=True,is_terminal=True)
        data = [o.get_json() for o in ad_list]
        for i in data:
            i.pop('is_active')
            i.pop('update_time')
            i.pop('create_time')
        return data
    def format_data(self, data):
        return ok_json(data = data)


list_ad_api = AdListAPI().wrap_func()
