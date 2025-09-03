import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .utils.jwt_custom import decode_token
from datetime import datetime, timezone
from django.conf import settings


User = get_user_model()


# class LibJWTAythentication(BaseAuthentication):
#     def authenticate(self,request):
#         auth_header = request.headers.get('Authorization')

#         if not auth_header:
#             return None
        
#         if not auth_header.startswith('Bearer '):
#             raise AuthenticationFailed('Invalid auth header format, Must be "Bearer -Token-"')
        
#         token = auth_header.split(' ')[1] #  base setting from custom auth

#         try:
#             payload = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms = ['HS256']
#             )

#             exp = payload.get('exp')

#             if exp and datetime.now(timezone.utc).timestamp()> exp:
#                 raise AuthenticationFailed('Token - expired')
            
#             user_id = payload.get('user_id')

#             if not user_id:
#                 raise AuthenticationFailed('Invalid token: no user found')
#             try:
#                 user = User.objects.get(id = user_id)
#             except User.DoesNotExist:
#                 raise AuthenticationFailed('User not found')

#             required_role = payload.get('role')

#             if required_role not in settings.ALLOWED_ROLES:
#                 raise AuthenticationFailed(f'Invalid role{required_role}')
            
#             return (user, token)
#         except jwt.DecodeError:
#             raise AuthenticationFailed('Invallid token')
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed('Invalid token signature')
        
    # def authenticate_header(self, request):
    #     return 'Bearer realm="api"'
    

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Invalid auth header format, Must be "Bearer -Token-"')
        
        token = auth_header.split(' ')[1]
        payload = decode_token(token)

        if not payload or payload.get('type') != 'access':
            raise AuthenticationFailed('Invalid or expired token')
        
        try:
            user = User.objects.get(id = payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        return(user, token)

