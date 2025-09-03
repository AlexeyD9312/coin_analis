from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_application.views import CoinInfoViewSet, CoinsDataViewSet 
from .views import CustomObtainAuthToken, CustomRefreshAuthToken, ProfileView, CustomObtainAuthToken, CustomRefreshAuthToken

router = DefaultRouter()
router.register(r'coin_info',CoinInfoViewSet )
router.register(r'coin_data',CoinsDataViewSet )

urlpatterns = [
    path('', include(router.urls)),
    #path('obtain_token/', ObtainAuthToken.as_view(), name = 'obtain-token'),
    path("api/custom/token/", CustomObtainAuthToken.as_view()),
    path("api/custom/token/refresh/", CustomRefreshAuthToken.as_view()),
    path("api/profile/", ProfileView.as_view()),
]