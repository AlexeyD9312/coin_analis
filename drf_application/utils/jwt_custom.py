import jwt, time
from django.conf import settings

cfg = settings.JWT_CUSTOM

def genarate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': int(time.time()) + cfg["ACCESS_TOKEN_LIFETIME"],
        'type':  'access'
    }
    return jwt.encode(payload, cfg['SECRET_KEY'], algorithm=cfg['ALGORITHM'])


def genarate_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': int(time.time()) + cfg["REFRESH_TOKEN_LIFETIME"],
        'type': 'refresh'
    }
    return jwt.encode(payload, cfg['SECRET_KEY'], algorithm=cfg['ALGORITHM'])

def decode_token(token):
    try:
        return jwt.decode(token, cfg['SECRET_KEY'], algorithm=[cfg['ALGORITHM']])
    except jwt.ExpiredSignatureError:
        None
    except jwt.InvalidTokenError:
        return None
        
