#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 机器模块所需公共api
"""
import random
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Channel,Machine

# 机器注册接口

class MachineCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'mac_address':'r',
        }

    def access_db(self, kwarg):
        mac_address = kwarg['mac_address']
        
        try:
            unique = Machine.objects.get(mac_address = mac_address)
            machine_id = unique.id

            info = {
                'machine_id':machine_id
                }
            data = info
            return data
        except Machine.DoesNotExist:
            address = "请完善信息"
            machine = Machine(mac_address=mac_address,address=address)
            machine.save()

            if machine:
                machine_id = machine.id

                info = {
                    'machine_id':machine_id
                    }
                data = info
                return data
            else:
                return None


    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('create faild')

create_machine_api = MachineCreateAPI().wrap_func()




# 开机密码修改接口

class PasswordUpdateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'new_password':'r',
            'machine_id':'r',
        }

    def access_db(self, kwarg):
        new_password = kwarg['new_password']
        machine_id = kwarg['machine_id']

        machine = Machine.objects.get(pk=machine_id)
        old_password = machine.password
        update_password = Machine.objects.filter(pk=machine_id).update(password=new_password)
        info = {
            'old_password':old_password,
            'new_password':new_password
        }

        return info


    def format_data(self, data):
        return ok_json(data = data)


update_password_api = PasswordUpdateAPI().wrap_func()
