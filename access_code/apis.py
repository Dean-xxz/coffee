#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 取货模块所需公共api
"""

from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Access_Code

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
        code = ''.join(random.sample(['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4','5','6','7','8','9','0'],6)).replace("", "")


    def format_data(self, data):
        return ok_json(data = data)

create_code_api = CodeCreateAP().wrap_func()


# 取货码创建接口

class CodeQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'item_id':'r',
        }

    def access_db(self, kwarg):


    def format_data(self, data):
        return ok_json(data = data)

query_code_api = CodeQueryAPI().wrap_func()