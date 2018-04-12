import json
from django.db import models
from utils.basemodel.base import BaseModel
from django.core import serializers

from product.models import Item
# Create your models here.

class Container(BaseModel):

    """
    咖啡机原料容器表
    """
    title = models.CharField(max_length=128,verbose_name="容器名称")
    size = models.IntegerField(verbose_name="容量(单位：g)")
    speed = models.DecimalField(max_digits = 10,decimal_places = 1,verbose_name="默认掉粉速度：单位（g/s）",null=True,blank=True)
    is_coffee = models.BooleanField(verbose_name='是否是咖啡盒',default = False)
    order = models.PositiveSmallIntegerField(verbose_name = "料盒顺序",default = 1,help_text = "面向机器，从右往左")
    remarks = models.TextField(verbose_name="备注、描述",null=True,blank=True,help_text="请输入备注、描述等")


    class Meta:
        verbose_name = "原料容器"
        verbose_name_plural = "原料容器"
        ordering = ["order",]

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Formula(BaseModel):
    """
    商品配方表，每一个商品条目都对应一个配方
    """

    item = models.ForeignKey("product.Item",verbose_name = "产品条目",related_name = "items")
    container = models.ForeignKey("Container",verbose_name= "原料容器",related_name="containers")
    consumption = models.PositiveSmallIntegerField(verbose_name="用量（单位：g）")
    effluentinterval = models.DecimalField(max_digits = 10,decimal_places = 2,verbose_name="出水间隔：单位（s）",null=True,blank=True)
   # dischargeperiod = models.DecimalField(max_digits = 10,decimal_places = 2,verbose_name='出料时间：单位（s）',null=True,blank=True)
    dischargemotorspeed = models.PositiveSmallIntegerField(verbose_name='料盒搅拌速度',default=50)
    mixermotorspeed = models.PositiveSmallIntegerField(verbose_name="搅拌机转速",null=True,blank=True)
    water = models.IntegerField(verbose_name="水量（单位：ml）",default=0)
    order = models.PositiveSmallIntegerField(verbose_name = "出料顺序",default = 1,help_text = "配方中原料的出料顺序")
    remarks = models.TextField(verbose_name="备注、描述",null=True,blank=True,help_text="请输入备注、描述等")

    class Meta:
        verbose_name = "独家配方"
        verbose_name_plural = "独家配方"
        ordering = ["item",'order']


#    def __str__(self):
#        return self.item

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data
