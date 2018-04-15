import json
from django.db import models
from utils.basemodel.base import BaseModel
from django.core import serializers
# Create your models here.
class Coupon(BaseModel):

    """
    优惠券
    """
    TYPE_CHOICES = (
            ('1',("打折券")),
            ('2',("满减券")),
            ('3',("代金券"))
        )

    title = models.CharField(verbose_name = "优惠券名称",max_length=128)
    descp = models.TextField(verbose_name="优惠券描述",null=True,blank=True)
    type = models.CharField(max_length=1,verbose_name="优惠券类型",choices=TYPE_CHOICES)
    dead_line = models.DateTimeField(blank=True,null=True,verbose_name="优惠截止日期")
    discounts = models.DecimalField(max_digits = 10,decimal_places = 1,verbose_name="折扣",null=True,blank=True,help_text="1折：1")
    cash = models.DecimalField(max_digits = 10,decimal_places = 2,verbose_name="代金券金额",null=True,blank=True)
    threshold = models.DecimalField(max_digits = 10,decimal_places = 2,verbose_name="满减券阈值",null=True,blank=True,help_text="满30-15，则填30")
    limit = models.DecimalField(max_digits = 10,decimal_places = 2,verbose_name="满减金额",null=True,blank=True,help_text="满30-15，则填15")


    class Meta:
        verbose_name = "优惠券"
        verbose_name_plural = "优惠券"
        ordering = ["-update_time",]

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data
