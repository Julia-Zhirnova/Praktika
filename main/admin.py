# main/admin.py

from django.contrib import admin
from .models import Sezon, Tip, PeriodyPraktiki
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

import pandas as pd
from django.http import HttpResponse

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'patronymic')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'patronymic', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'patronymic', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('kod_tipa', 'naimenovanie_tipa')

@admin.register(Sezon)
class SezonAdmin(admin.ModelAdmin):
    list_display = ('kod_sezona', 'naimenovanie_sezona')



@admin.register(PeriodyPraktiki)
class PeriodyPraktikiAdmin(admin.ModelAdmin):
    list_display = ('nomer_perioda', 'sezon_kod', 'god', 'obem_v_chasah', 'data_nachala',
                    'data_vydachi_zadaniya', 'data_okonchaniya', 'tip_kod')
'''
    actions = ['export_to_excel', 'import_from_excel']

    def export_to_excel(self, request, queryset):
        import pandas as pd
        from django.http import HttpResponse

        data = []
        for obj in queryset:
            data.append({
                'Nomer_perioda': obj.nomer_perioda,
                'Sezon_kod': obj.sezon_kod.naimenovanie_sezona,
                'God': obj.god,
                'Obem_v_chasah': obj.obem_v_chasah,
                'Data_nachala': obj.data_nachala,
                'Data_vydachi_zadaniya': obj.data_vydachi_zadaniya,
                'Data_okonchaniya': obj.data_okonchaniya,
                'Tip_kod': obj.tip_kod.naimenovanie_tipa if obj.tip_kod else None,
            })

        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=periody_praktiki.xlsx'
        df.to_excel(response, index=False)
        return response

    export_to_excel.short_description = 'Экспорт выбранных записей в Excel'

    def import_from_excel(self, request):
        if request.method == 'POST':
            file = request.FILES['file']
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                sezon = Sezon.objects.get_or_create(naimenovanie_sezona=row['Sezon_kod'])[0]
                tip = Tip.objects.get_or_create(kod_tipa=row['Tip_kod'])[0]
                PeriodyPraktiki.objects.create(
                    sezon_kod=sezon,
                    god=row['God'],
                    obem_v_chasah=row['Obem_v_chasah'],
                    data_nachala=row['Data_nachala'],
                    data_okonchaniya=row['Data_okonchaniya'],
                    tip_kod=tip
                )
            self.message_user(request, "Данные успешно импортированы")
            return redirect("..")
        return render(request, 'admin/import_excel.html')

    import_from_excel.short_description = 'Импорт данных из Excel'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.import_from_excel, name='import_excel'),
        ]
        return custom_urls + urls
        '''
