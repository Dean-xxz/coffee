import json
from django.db import models
from utils.basemodel.base import BaseModel
from django.core import serializers
from formula.models import Container

# Create your models here.

class Channel(BaseModel):

    """
    咖啡机经销商户、渠道
    """
    title = models.CharField(max_length=128,verbose_name="渠道名称",null=True,blank=True)
    username = models.CharField(max_length=24,verbose_name="用户名",null=True,blank=True)
    password = models.CharField(max_length=24,verbose_name="商户登录密码",null=True,blank=True)
    mobile = models.CharField(max_length=12,verbose_name="服务热线",null=True,blank=True)
    remarks = models.TextField(verbose_name="渠道简介",null=True,blank=True,help_text="请输入商户简介")


    class Meta:
        verbose_name = "经销渠道"
        verbose_name_plural = "经销渠道"
        ordering = ["-create_time",]

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Machine(BaseModel):
    """
    咖啡机信息
    """

    ERROR_CHOICES = (
            ('1',("正常")),
            ('2',("故障")),
        )

    MATERIAL_CHOICES = (
            ('1',("物料充足")),
            ('2',("余量较少")),
            ('3',("余量不足"))
        )
    channel = models.ForeignKey("Channel",verbose_name = "经销渠道",related_name = "machine_channel",null=True,blank=True)
    province = models.CharField(max_length=32,verbose_name="省份（eg:广东省）",null=True,blank=True)
    city = models.CharField(max_length=32,verbose_name="市（eg:深圳市）",null=True,blank=True)
    address = models.CharField(max_length=128,verbose_name="详细机器位置：eg：深大2号楼",null=True,blank=True)
    mac_address = models.CharField(max_length=128,verbose_name="机器唯一编码",unique=True)
    password = models.CharField(max_length=6,verbose_name="开机密码",default='zk8888')
    is_networking = models.BooleanField(verbose_name="机器是否联网",default=True)
    error_state = models.CharField(max_length=1,verbose_name="故障状态",default=1,choices=ERROR_CHOICES)
    material_state = models.CharField(max_length=1,verbose_name="物料状态",default=1,choices=MATERIAL_CHOICES)


    class Meta:
        verbose_name = "机器信息"
        verbose_name_plural = "机器信息"
        # ordering = ["-create_time",]

    def __str__(self):
        return self.address

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Machine_state(BaseModel):

    """
    机器日志状态表，记录机器日志
    """
    machine = models.ForeignKey("Machine",related_name="machine_state",verbose_name="机器")
    state_id = models.IntegerField(verbose_name="状态id",null=True,blank=True)
    code = models.CharField(max_length=32,verbose_name="状态码")
    descp = models.CharField(max_length=128,verbose_name="状态描述")
    is_cannel = models.BooleanField(verbose_name="是否清楚",default=False)

    class Meta:
        verbose_name = "机器状态"
        verbose_name_plural = "机器状态"
        ordering = ["-create_time",]

    def __str__(self):
        return self.descp

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data



class Material_state(BaseModel):
    """
    料盒状态
    """
    machine = models.ForeignKey("Machine",related_name="machine_material",verbose_name="机器")
    containerid = models.IntegerField(verbose_name="料盒id",null=True,blank=True)
    container = models.ForeignKey("formula.Container",related_name="container_state",verbose_name="容器",null=True,blank=True)
    margin = models.CharField(max_length=12,verbose_name="料盒余量",null=True,blank=True)

    class Meta:
        verbose_name = "料盒状态"
        verbose_name_plural = "料盒状态"
        ordering = ["-create_time",]

    def __str__(self):
        return self.margin

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data