#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 机器模块所需公共api
"""
import random
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Channel,Machine,Machine_state,Material_state
from formula.models import Container

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


# 机器日志上传接口

class LogCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'machine_id':'r',
            'status':'r',
            'descp':'r',
        }

    def access_db(self, kwarg):
        machine_id = kwarg['machine_id']
        status = kwarg['status']
        descp = kwarg['descp']
        
        machine_state = Machine_state(machine_id = machine_id,descp=descp)
        machine_state.save()
        if machine_state:
            update_status = Machine.objects.filter(pk = machine_id).update(error_state = status)


        return 'create successful'


    def format_data(self, data):
        return ok_json(data = data)


create_log_api = LogCreateAPI().wrap_func()


#日志清除接口
class LogDeleteAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'machine_id':'r',
        }

    def access_db(self, kwarg):
        machine_id = kwarg['machine_id']

        machine_state = Machine_state.objects.filter(machine_id = machine_id).update(is_cannel = True)
        machine_status = Machine.objects.filter(pk = machine_id).update(error_state = '1')

        return 'update successful'


    def format_data(self, data):
        return ok_json(data = data)


delete_log_api = LogDeleteAPI().wrap_func()


#物料状态上传接口
class MaterialUpdateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'machine_id':'r',
            'margin':'r',
        }

    def access_db(self, kwarg):
        machine_id = kwarg['machine_id']
        margin = kwarg['margin']
        margin = eval(margin)
        for key, value in margin.items():
            containerid = key
            container = Container.objects.get(order = containerid)
            container_id = container.id    
            margin = margin[key]

            try:
                material = Material_state.objects.get(machine_id = machine_id,containerid = containerid)
                material = Material_state.objects.filter(machine_id = machine_id,containerid = containerid).update(margin = margin)
                return 'create or update successful'
            except Material_state.DoesNotExist:
                material_state = Material_state(machine_id = machine_id,containerid = containerid,container_id = container_id,margin = margin)
                material_state.save()
                return 'create or update successful'


    def format_data(self, data):
        return ok_json(data = data)


update_material_api = MaterialUpdateAPI().wrap_func()


#商户平台登录
class MchLoginAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'username':'r',
            'password':'r',
        }

    def access_db(self, kwarg):
        username = kwarg['username']
        password = kwarg['password']

        try:
            channel = Channel.objects.get(username = username)
            psd = channel.password
            if psd == password:
                data = channel.get_json()
                data.pop('create_time')
                data.pop('update_time')
                data.pop('is_active')
                data.pop('password')
                data['mch_id'] = data['id']
                data.pop('id')

                return data
            else:
                return None

        except Channel.DoesNotExist:
            return None

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('username or password is error')

login_mch_api = MchLoginAPI().wrap_func()

#商户修改密码接口
class MchPsdUpdateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'old_password':'r',
            'new_password':'r',
            'mch_id':'r',
        }

    def access_db(self, kwarg):
        old_password = kwarg['old_password']
        new_password = kwarg['new_password']
        mch_id = kwarg['mch_id']
        channel = Channel.objects.get(pk=mch_id)
        psd = channel.password
        if psd == old_password:
            update_psd = Channel.objects.filter(pk=mch_id).update(password = new_password)
            return 'password update successful'
        else:
            return None

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('password update faild')

update_mchpsd_api = MchPsdUpdateAPI().wrap_func()


#商户列表接口
class MchListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
        }

    def access_db(self, kwarg):
        mch_list = Channel.objects.filter(is_active=True)
        mch_list = [o.get_json() for o in mch_list]
        for i in mch_list:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            i.pop('password')
            i['mch_id'] = i['id']
            i.pop('id')
        return mch_list

    def format_data(self, data):
        return ok_json(data = data)

list_mch_api = MchListAPI().wrap_func()


#机器列表接口
class MachineListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'mch_id':'r',
        }

    def access_db(self, kwarg):
        mch_id = kwarg['mch_id']
        machine_list = Machine.objects.filter(channel_id = mch_id,is_active=True)
        machine_list = [o.get_json() for o in machine_list]
        for i in machine_list:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            i['mch_id'] = i['channel']
            i['machine_id'] = i['id']
            i.pop('id')
            i.pop('channel')
        return machine_list

    def format_data(self, data):
        return ok_json(data = data)

list_machine_api = MachineListAPI().wrap_func()

#筛选条件产品列表
class ProductListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
        }

    def access_db(self, kwarg):
        product_list = Product.objects.filter(is_terminal=True,is_active=True)
        product_list = [o.get_json() for o in product_list]
        for i in machine_list:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            i.pop('')
            i['product_id'] = i['id']
            i.pop('id')
        return machine_list

    def format_data(self, data):
        return ok_json(data = data)

list_product_api = ProductListAPI().wrap_func()



