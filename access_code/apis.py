#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 取货模块所需公共api
"""
import random
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Access_Code
from product.models import Item

# 取货码创建接口

class CodeCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'item_id':'r',
            'user_id':('o',None),
        }

    def access_db(self, kwarg):
        item_id = kwarg['item_id']
        user_id = kwarg['user_id']
        code = ''.join(random.sample(['A', 'B', 'C', 'D', 'E', 'F', '1', '2', '3', '4','5','6','7','8','9','0'],6)).replace("", "")

        access_code = Access_Code(item_id = item_id,user_id = user_id,code = code)
        access_code.save()

        info = {
            'code':code
            }
        data = info

        return data


    def format_data(self, data):
        return ok_json(data = data)

create_code_api = CodeCreateAPI().wrap_func()


# 取货码验证接口


class CodeQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'code':'r',
        }

    def access_db(self, kwarg):
        code = kwarg['code']

        try:
            code = Access_Code.objects.get(code = code,status=False)
            data = code.get_json()
            data['return_message'] = 'Verification successful'
            item_id = data['item']
            item = Item.objects.get(pk=item_id)
            item_detail = item.get_json()
            data['item_detail'] = item_detail
            data.pop('create_time')
            data.pop('update_time')
            data.pop('is_active')
            return data
        except Access_Code.DoesNotExist:
            return None


    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('Verification failure')


query_code_api = CodeQueryAPI().wrap_func()

class CodeUpdateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'code':'r',
        }

    def access_db(self, kwarg):
        code = kwarg['code']

        try:
            code = Access_Code.objects.get(code = code,status=False)
            status_update = Access_Code.objects.filter(code = code).update(status=True)
            data = "update successful"
            return data
        except Access_Code.DoesNotExist:
            return None


    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('code is error')

update_code_api = CodeUpdateAPI().wrap_func()
