import json
from urllib.request import urlopen
from django.core.cache import cache

#config
appid = "wxc59b077d6c26e6ff"
app_secret = "8050cb55bd7eed9ce2959b3c8f11e3af"

access_token_key = 'WECHAT_ACCESS_TOKEN'

def get_access_token(code):
    appid = 'wxc59b077d6c26e6ff'
    secret = '8050cb55bd7eed9ce2959b3c8f11e3af'
    code = code
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(appid,secret,code)
    res = urlopen(url).read().decode("utf8")
    message = json.loads(res)
    refresh_token = message['refresh_token']
    url = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token&refresh_token=%s"%(appid,refresh_token)
    res = urlopen(url).read().decode("utf8")
    data = json.loads(res)
    openid = data['openid']
    access_token = data['access_token']
    info = {
        "openid":openid,
        "access_token":access_token
    }
    return info

def get_userinfo(access_token,openid):
    appid = 'wxc59b077d6c26e6ff'
    secret = '8050cb55bd7eed9ce2959b3c8f11e3af'
    access_token = access_token
    openid = openid
 
    url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"%(access_token,openid)
    res = urlopen(url).read().decode("utf8")
    message = json.loads(res)
    data = message

    return data

