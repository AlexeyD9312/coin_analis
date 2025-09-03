from rest_framework import serializers 
from coin_app.models import CoinInfo, CoinsData


class CoinInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoinInfo
        fields ='__all__'


class CoinDataSerializers(serializers.ModelSerializer):
    coin_info = CoinInfoSerializers(source = 'coin', read_only = True)# from reading GET
    coin = serializers.SlugRelatedField(
        slug_field =  'ticker' ,                      #PUT POST
        queryset = CoinInfo.objects.all()
    )
    class Meta:
        model = CoinsData
        fields = [
            'id',
            'coin',
            'coin_info',
            'Name',
            'ticker',
            'interval',
            'timestamp',
            'open_price',
            'hihg_price',
            'low_price',
            'close_price',
            'vwap',
            'volume',
            'trade_count',
        ]