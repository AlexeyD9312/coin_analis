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
from drf_application.auth import LibJWTAythentication
from rest_framework.permissions import IsAuthenticated
from .auth import CustomJWTAuthentication
from .utils.jwt_custom import genarate_access_token, genarate_refresh_token, decode_token


class CoinInfoViewSet(viewsets.ModelViewSet):
    queryset = CoinInfo.objects.all()
    serializer_class = CoinInfoSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['foundation_year']


class CoinsDataViewSet(viewsets.ModelViewSet):
    #permission_classes = [AllowAny]
    authentication_classes =[LibJWTAythentication]
    queryset = CoinsData.objects.all()
    serializer_class = CoinDataSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Name']


class ObtainAuthToken(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password = password)
        if user:
            token, created = Token.objects.get_or_create(user = user)
            return Response({'token':token.key})
        return Response({'error':'Invalid credentials'},status = 400)
    

class CustomObtainAuthToken(APIView):

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password = password)
        if not user:
            return Response({'error': 'Invallid credentional'}, status=400)
        access_token = genarate_access_token(user.id)    
        refresh_token = genarate_refresh_token(user.id) 

        return Response({'access': access_token, 'refresh': refresh_token}) 
    

class CustomRefreshAuthToken(APIView):

    def post(self,request):
        refresh = request.data.get('refresh')
        payload = decode_token(refresh)

        if not payload or payload.get('type') !='refresh':
            return Response({'detail': 'Invalid,expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        access = genarate_access_token(payload['user_id'])
        return Response({'access': access})


class ProfileView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'username': request.user.username})
