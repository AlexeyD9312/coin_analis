import os
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from coin_app.models import UploadedFiles
from django.contrib import admin
from .models import CoinsData, CoinInfo
from .admin_mixins import ExportCsvMixin, EditableFieldsMixin, YearListFilter



def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if not file.name.endwith('.txt'):
            return JsonResponse({'Error invalid ststus TXT'})
        try:
            content = file.read().decode('utf-8')
            word_count = len(content.split())
            char_count = len(content)

            uploaded_files = UploadedFiles.objects.create(
                file = file,
                filename = file.name,
                word_count = word_count,
                char_count = char_count
            )
             
            return JsonResponse({
                'id':upload_file.id,
                'filename': upload_file.filename,
                'word_count' : word_count,
                'char_count' : char_count
            })
        except Exception as e:
            return JsonResponse({'error':str(e)}, status = 500)
    return JsonResponse({'error': 'No file provided'}, status = 400)


def list_file(request ):
    files = UploadedFiles.objects.all().order_by('-uploaded_at')
    file_list = [{
        'id': f.id,
        'filename':f.filename,
        'word_count' : f.word_count,
        'char_count' : f.char_count
    } for f in files]
    return JsonResponse({'files': file_list})

def view_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFiles, id = file_id)
    try:
        with uploaded_file.file.open('r') as f:
            content = f.read().decode('utf-8')
        return JsonResponse({
                'id':upload_file.id,
                'filename': upload_file.filename,
                'content':content,
                'word_count' : upload_file.word_count,
                'char_count' : upload_file.char_count
            })
    except Exception as e:
            return JsonResponse({'error':str(e)}, status = 500)
    

def delete_file(request, file_id):
    if request.method == 'POST':
        uploaded_file = get_object_or_404(UploadedFiles, id = file_id)
        try:
            uploaded_file.delete()
            return JsonResponse({'massage':'File delete'})
        except Exception as e:
            return JsonResponse({'error':'Invalid request method'}, status = 500)




#@admin.register(CoinsData)
class CoinAdmin(ExportCsvMixin, EditableFieldsMixin, admin.ModelAdmin):
    export_fields = ['Ticker','timestamp','open_price','close_price','volume']
    editable_fields = ('open_price','close_price','volume')
    actions = ['export_to_csv']
    list_display = ('Name','Ticker','interval','timestamp','open_price','hihg_price','low_price','close_price','vwap','volume','trade_count')
    search_fields = ('Name','Ticker')

#@admin.register(CoinInfo)
class CoinInfoAdmin(YearListFilter, admin.ModelAdmin):
    list_display = ('ticker','name','logo','foundation_year','founder','description')
    search_fields = ('ticker','name')
    YearListFilter.fields_name = 'foundation_year'