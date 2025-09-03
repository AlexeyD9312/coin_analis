from rest_framework import viewsets,status
from rest_framework.response import Response 
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import CoinInfoSerializers, CoinDataSerializers
from coin_app.models import CoinInfo, CoinsData
#from drf_application.auth import LibJWTAythentication
from rest_framework.permissions import IsAuthenticated
from .auth import CustomJWTAuthentication
from .utils.jwt_custom import generate_access_token, generate_refresh_token, decode_token


class CoinInfoViewSet(viewsets.ModelViewSet):
    queryset = CoinInfo.objects.all()
    serializer_class = CoinInfoSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['foundation_year']


class CoinsDataViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes =[CustomJWTAuthentication]
    queryset = CoinsData.objects.all()
    serializer_class = CoinDataSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Name']


# class ObtainAuthToken(APIView):
#     permission_classes = [AllowAny]

#     def post(self,request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password = password)
#         if user:
#             token, created = Token.objects.get_or_create(user = user)
#             return Response({'token':token.key})
#         return Response({'error':'Invalid credentials'},status = 400)
    

class CustomObtainAuthToken(APIView):
    permission_classes = [AllowAny]  # публичный эндпоинт

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)

        return Response({'access': access_token, 'refresh': refresh_token})



class CustomRefreshAuthToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=400)

        payload = decode_token(refresh_token)
        if not payload:
            return Response({'error': 'Invalid token'}, status=401)

        if payload.get('type') != 'refresh':
            return Response({'error': 'Invalid token type'}, status=401)

        user_id = payload.get('user_id')
        if not user_id:
            return Response({'error': 'Token has no user ID'}, status=401)

        access_token = generate_access_token(user_id)
        return Response({'access': access_token})



class ProfileView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'email': request.user.email})