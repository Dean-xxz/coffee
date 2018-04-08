import json
from django.db import models
from utils.basemodel.base import BaseModel
from django.core import serializers

# Create your models here.

class Channel(BaseModel):

    """
    咖啡机经销商、渠道
    """
    title = models.CharField(max_length=128,verbose_name="渠道名称",null=True,blank=True)
    remarks = models.TextField(verbose_name="渠道简介",null=True,blank=True,help_text="请输入渠道简介")


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
    channel = models.ForeignKey("Channel",verbose_name = "经销渠道",related_name = "machine_channel",null=True,blank=True)
    address = models.CharField(max_length=128,verbose_name="机器位置：eg：深圳-深大-2号楼",null=True,blank=True)
    mac_address = models.CharField(max_length=128,verbose_name="机器唯一编码",unique=True)
    password = models.CharField(max_length=6,verbose_name="开机密码",default='zk8888')


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