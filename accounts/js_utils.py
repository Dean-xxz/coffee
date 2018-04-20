import json
import string
import hashlib
import random
from urllib.request import urlopen
from django.core.cache import cache
from django.utils.timezone import now

appid = 'wxc59b077d6c26e6ff'
secret = '8050cb55bd7eed9ce2959b3c8f11e3af'

access_token_key = 'WECHAT_ACCESS_TOKEN'
def get_new_access_token():
    # 获取新的access_token,这个和获取用户信息的access_token 是不同的
    access_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(appid,secret)
    res = urlopen(access_token_url).read().decode("utf8")
    message = json.loads(res)
    ACCESS_TOKEN = message['access_token']
    cache.set(access_token_key,ACCESS_TOKEN,message['expires_in'] - 20)
    return ACCESS_TOKEN

def get_access_token():
    """
    获取缓存的微信全局access_token
    """
    ACCESS_TOKEN = cache.get(access_token_key)
    if not ACCESS_TOKEN:
      ACCESS_TOKEN = get_new_access_token()
      return ACCESS_TOKEN
    return ACCESS_TOKEN

js_ticket_key = 'WECHAT_JS_TICKET'
def get_new_js_ticket():
    # 获取一个新的票据
    ACCESS_TOKEN = get_access_token()
    ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"%ACCESS_TOKEN
    res = urlopen(ticket_url).read().decode("utf8")
    message = json.loads(res)
    TICKET = message['ticket']
    cache.set(js_ticket_key,TICKET,message['expires_in'])
    return TICKET

def get_js_ticket():
    TICKET = cache.get(js_ticket_key)
    if not TICKET:
        TICKET = get_new_js_ticket()

    return TICKET

def get_js_config(url):
    noncestr = ''.join(random.sample(string.ascii_letters+string.digits,16))
    timestamp = int(now().timestamp())
    jsapi_ticket= get_js_ticket()

    string1 = "jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s"%(jsapi_ticket,noncestr,timestamp,url)
    signature = hashlib.sha1(string1.encode('utf-8')).hexdigest()
    info = {
        "timestamp":timestamp,
        "nonceStr":noncestr,
        "jsapi_ticket":jsapi_ticket,
        "signature":signature,
        "appId":appid
    }
    return info
