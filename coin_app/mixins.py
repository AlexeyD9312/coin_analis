from django.utils.dateparse import parse_datetime
from django.db.models import Avg, Max, Min, Count
import csv
import json
from django.http import HttpResponse
import pandas as pd
import logging


class CoinDataFilterMixin:
    """
    Фильтрация  по GET 
    """
    def filter_queryset(self, queryset):
        ticker = self.request.GET.get('ticker')
        interval = self.request.GET.get('interval')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')

        if ticker:
            queryset = queryset.filter(Ticker__iexact=ticker)
        if interval:
            queryset = queryset.filter(interval=interval)
        if start:
            queryset = queryset.filter(timestamp__gte=parse_datetime(start))
        if end:
            queryset = queryset.filter(timestamp__lte=parse_datetime(end))

        return queryset
    


class CoinStatsMixin:
    """
    статистикa по queryset.
    """
    def get_stats(self, queryset):
        return queryset.aggregate(
            avg_open=Avg('open_price'),
            avg_close=Avg('close_price'),
            max_high=Max('hihg_price'),
            min_low=Min('low_price'),
            avg_volume=Avg('volume'),
            trade_count=Count('id')
        )
    


class DataExportMixin:
    """
     экспорт queryset в CSV  
    """
    export_fields = []

    def export_csv(self, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="coins.csv"'
        writer = csv.writer(response)
        writer.writerow(self.export_fields)
        for obj in queryset.values_list(*self.export_fields):
            writer.writerow(obj)
        return response

    def export_json(self, queryset):
        data = list(queryset.values(*self.export_fields))
        return HttpResponse(json.dumps(data), content_type='application/json')
    


class MLPreprocessMixin:
    """
    queryset в pandas.DataFrame  
    """
    def to_dataframe(self, queryset):
        df = pd.DataFrame(list(queryset.values()))
        return df.dropna()

    def normalize(self, df, fields):
        """Z-score нормализация"""
        df[fields] = (df[fields] - df[fields].mean()) / df[fields].std()
        return df
    


logger = logging.getLogger(__name__)

class RequestLoggingMixin:
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"{request.method} {request.path} user={request.user}")
        return super().dispatch(request, *args, **kwargs)