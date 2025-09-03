import jwt, time
from django.conf import settings

cfg = settings.JWT_CUSTOM

def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': int(time.time()) + int(cfg["ACCESS_TOKEN_LIFETIME"].total_seconds()),
        'type':  'access'
    }
    return jwt.encode(payload, cfg['SECRET_KEY'], algorithm=cfg['ALGORITHM'])


def generate_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': int(time.time()) + int(cfg["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        'type': 'refresh'
    }
    return jwt.encode(payload, cfg['SECRET_KEY'], algorithm=cfg['ALGORITHM'])

def decode_token(token):
    try:
        return jwt.decode(token, cfg['SECRET_KEY'], algorithms=[cfg['ALGORITHM']])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
        
