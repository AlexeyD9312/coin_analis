from django.contrib import admin
from coin_app.models import CoinsData, CoinInfo, UploadedFiles
from django import forms
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.admin.widgets import AdminDateWidget
import csv
from django.utils.safestring import mark_safe
from django.db.models.functions import ExtractYear
from django.forms import DateTimeInput 
from .admin_mixins import YearListFilter,ExportCsvMixin,EditableFieldsMixin,ExportJsonMixin,ImportCsvMixin


class CoinAdminForm(forms.ModelForm):
    class Meta:
        model = CoinsData
        fields = '__all__'
        #widgets = {
       #    # 'timestamp': DateTimeInput( attrs= {'class' : 'vDateTimeField'})          
        #}
    

class CoinInfoAdminForm(forms.ModelForm):
    class Meta:
        model = CoinInfo
        fields = '__all__'
       # widgets = {
            
       #     'description' : forms.Textarea(attrs={'rows':5, 'cols':35})
       # }

    def clean_ticker(self):
        ticker = self.cleaned_data.get('ticker')
        if len(ticker) > 8:
            raise forms.ValidationError('ticker must be less on 8 chars')
        return ticker


class CreateYearsFilter(admin.SimpleListFilter):
    title = 'Foundation years'
    parameter_name = 'foundation_year'

    def lookups(self, request, model_admin):
        years = CoinInfo.objects.values_list( 'foundation_year', flat= True).distinct()
        return [(str(y), str(y)) for y in years if y]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(foundation_year__year =self.value())
        return queryset

@admin.register(CoinsData)
class CoinAdmin(ExportCsvMixin, EditableFieldsMixin,ExportJsonMixin,ImportCsvMixin, admin.ModelAdmin):
    form = CoinAdminForm
    list_display = ('Name','ticker','interval','timestamp', 'open_price', 'hihg_price','low_price','close_price','vwap','volume','trade_count')   
    #list_editable = ('open_price','close_price','volume')
    list_filter = ('open_price','close_price' )
    search_fields = ('Name','ticker')
    fields =('Name','ticker','interval', 'open_price', 'hihg_price','low_price','close_price','vwap','volume','trade_count')

    export_fields = ['Name','ticker','interval', 'open_price', 'hihg_price','low_price','close_price','vwap','volume','trade_count']
    export_json_fields = ['Name','ticker','interval', 'open_price', 'hihg_price','low_price','close_price','vwap','volume','trade_count']

    actions = ['export_to_csv','export_to_json']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-csv/',
                self.admin_site.admin_view(self.import_from_csv),
                name = 'coinsdata_import_csv'
            ),
        ]
        return custom_urls + urls 

    change_list_template = 'admin/coins_list.html'

    #def export_to_csv(self,request,queryset):
    #    response = HttpResponse(content_type = 'text/csv')
    #    response['Content-Disposition'] = 'attachment; filename="coins_export.csv"'
    #    writer = csv.writer(response)
    #    writer.writerow(['ticker','timestamp','open_price','close_price','volume'])
    #    for coin in queryset:
    #        writer.writerow([coin.ticker, coin.timestamp, coin.open_price, coin.close_price, coin.volume])
    #    return response
    #export_to_csv.short_description = 'Export selected coins to csv'

    
    #change_list_template = None
    #change_form_template = None #'admin/coin_change_form.html'

   # class Media:
   #     css = {
   #         'all':('admin/css/coin_admin.css',),
    #    }
    #    js = ('admin/js/coins_admin.js',)
    
    #def get_urls(self):
    #    return super().get_urls()
    #    custome_urls = [ 
    #        path('dashbord/', self.admin_site.admin_view(self.dashboard_view)),
    #    ]
     #   return custome_urls + urls

    #def dashboard_view(self, request):
    #    total_coins = CoinsData.objects.count()
     #   context = {
    #        'total_coins' : total_coins
     #   }
     #   return TemplateResponse(request, 'admin/coin_dashboard.html', context)


@admin.register(CoinInfo)
class CoinInfoAdmin(ExportCsvMixin, EditableFieldsMixin,ExportJsonMixin, ImportCsvMixin ,admin.ModelAdmin):
    form = CoinInfoAdminForm
    list_display = ('ticker','name','logo','foundation_year','founder','description')   
    #list_editable = ('foundation_year','founder','description')
    list_filter = ( YearListFilter,)
    search_fields = ('ticker','name')

    fieldsets = (
        ('Basic info',{
            'fields': ('ticker','name','description'),
            'description' : 'Enter your info'
        }),
        ('Details', {
            'fields': ('foundation_year','founder'),
            'classes':('collapse',),

        }),    
       # ('Cover',{
       #     'fields':('cover','cover_preview' ),
       #     'description': 'upload coin cover'
       # }),
    )
    export_fields = ['ticker','name','logo','foundation_year','founder','description']
    export_json_fields = ['ticker','name','logo','foundation_year','founder','description']
    actions = ['export_to_csv','export_to_json']

admin.site.register(UploadedFiles)

    

