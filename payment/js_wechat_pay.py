#__author__="Dean"

import hashlib
from random import Random
import time
import xmltodict
import requests
import json
from dict2xml import dict2xml
from .pay_settings import WECHAT_PAY_CONFIG

config = WECHAT_PAY_CONFIG

    #构建签名
def build_sign(params):
    # 对所有传入参数按照字段名的 ASCII 码从小到大排序（字典序）
    # keys = params.keys()
    # keys.sort()
    # sorted(keys)

    array = []
    for key in sorted(params.keys()):
    # for key in keys:
        # 值为空的参数不参与签名
        if params[key] == None or params[key] == '':
            continue
        # sign不参与签名
        if key == 'sign':
            continue
        array.append("%s=%s" % (key, params[key]))
    # 使用 URL 键值对的格式拼接成字符串string1
    string1 = "&".join(array)

    # 在 string1 最后拼接上 key=Key(商户支付密钥)得到 stringSignTemp 字符串
    stringSignTemp = string1 + '&key=' + config['key']

     # 对 stringSignTemp 进行 md5 运算，再将得到的字符串所有字符转换为大写
    if isinstance(stringSignTemp, str):
        stringSignTemp = stringSignTemp.encode('utf-8')
    m = hashlib.md5(stringSignTemp)
    return m.hexdigest().upper()
#    return m.hexdigest()

    #构建统一下单接口需要参数
def build_unifiedorder(params):
    base_params = {
        'appid': config['appid'],
        'mch_id': config['mch_id'],
        'nonce_str': generate_random_string(),
        'trade_type': 'JSAPI',
        'body': params['body'],
        'out_trade_no': params['out_trade_no'],
        'total_fee': params['total_fee'],
        'spbill_create_ip': params['spbill_create_ip'],
        'notify_url': config['notify_url'],
        'openid': params['openid']
    }

    base_params['sign'] = build_sign(base_params)
    return dict_to_xml(base_params)


    #构建随机字符串none_str
def generate_random_string(randomlength=32):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

    #dict转xml方法
def dict_to_xml(params):
    xml_elements = ["<xml>",]
    for (k, v) in params.items():
        if str(v).isdigit():
            xml_elements.append('<%s>%s</%s>' % (k, v, k))
        else:
            xml_elements.append('<%s><![CDATA[%s]]></%s>' % (k, v, k))
    xml_elements.append('</xml>')
    return ''.join(xml_elements)


    #调起支付
def build_form_by_prepay_id(prepay_id):
    base_params = {
        'appId': config['appid'],
        'timeStamp': str(int(time.time())),
        'nonceStr': generate_random_string(),
        'package': "prepay_id=%s" % prepay_id,
        'signType': "MD5"
    }
    base_params['paySign'] = build_sign(base_params)
    return base_params


    #实际app支付方法
def build_form_by_params_js(params):
    headers = {'Content-Type': 'application/xml'}
    xml = build_unifiedorder(params)
    if isinstance(xml, str):
        xml = xml.encode('utf-8')
    response = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=xml, headers=headers)
    response.encoding = 'utf-8'
    response_dict = xmltodict.parse(response.text)['xml']
    print (response_dict)
    if response_dict['return_code'] == 'SUCCESS':
        return build_form_by_prepay_id(response_dict['prepay_id'])




def notify_string_to_params(string):
    params = {}
    key_value_array = string.split('&')
    for item in key_value_array:
        key, value = item.split('=')
        params[key] = value
    return params

def verify_notify_string(string):
    params = notify_xml_string_to_dict(string)

    notify_sign = params['sign']
    del params['sign']

    if build_sign(params) == notify_sign:
        return True
    return False

def notify_xml_string_to_dict(string):
    xml_data = xmltodict.parse(string)['xml']
    params = {}
    for k in xml_data:
        params[k] = xml_data[k]
    return params

def notify_success_xml():
    ret_dict = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK',
            }
    xml_str = dict2xml(ret_dict, wrap='xml')
    return xml_str


# if __name__ == '__main__':
#
#     params = build_form_by_params({
#         'body': 'test',
#         'out_trade_no': 'id',
#         'total_fee': '1',
#         'spbill_create_ip': '127.0.0.1',
#         'openid': 'o5juAt-FpI1i43FCUYT1WbIsc0BU'
#         })
#
#     print json.dumps(params)


