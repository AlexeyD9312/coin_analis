import csv
from django.http import HttpResponse
from django.contrib import admin
import json
from django.template.response import TemplateResponse
from django.contrib import messages

#    CSV
class ExportCsvMixin:
    export_fields = []

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        writer.writerow(self.export_fields)
        for obj in queryset.values_list(*self.export_fields):
            writer.writerow(obj)
        return response

    export_to_csv.short_description = 'Export selected items to CSV'

#  Редактируемые поля
class EditableFieldsMixin:
    editable_fields = ('interval','timestamp', 'open_price', 'hihg_price','low_price','close_price','vwap','volume','trade_count','foundation_year','founder','description')

    def get_list_editable(self, request):
        return self.editable_fields

# Фильтр по году
class YearListFilter(admin.SimpleListFilter):
    title = 'Year'
    parameter_name = 'year'
    field_name = 'foundation_year'  # поле модели 

    def lookups(self, request, model_admin):
        if not self.field_name:
            return []
        qs = model_admin.model.objects.values_list(self.field_name, flat=True).distinct()
        return [(str(y), str(y)) for y in qs if y]

    def queryset(self, request, queryset):
        if self.value() and self.field_name:
            return queryset.filter(**{f"{self.field_name}": self.value()})
        return queryset


class ExportJsonMixin:
    export_json_fields = []

    def export_to_json(self, request, queryset):
        data = list(queryset.values(*self.export_json_fields))
        response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="export.json"'
        return response

    export_to_json.short_description = "Export selected items to JSON"



class ImportCsvMixin:
    def import_from_csv(self, request):
        if request.method == 'POST' and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            created = updated = 0
            for row in reader:
                obj, created_flag = self.model.objects.update_or_create(
                    ticker=row.get('ticker'),  #   для объекта 
                    defaults=row
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1
            self.message_user(
                request,
                f"CSV imported successfully: {created} created, {updated} updated.",
                level=messages.SUCCESS
            )
        context = dict(
            self.admin_site.each_context(request),
        )
        return TemplateResponse(request, "admin/import_csv.html", context)

    import_from_csv.short_description = "Import from CSV"