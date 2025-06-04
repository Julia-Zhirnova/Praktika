# main/admin.py

from django.contrib import admin
from .models import Sezon, Tip, PeriodyPraktiki, Specialnosti, SpecialnostiGruppy, UchebnyjPlan, ProfessionalnyeModuli, Praktiki, RukovoditeliPraktik, Zadaniya 
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
    

@admin.register(Specialnosti)
class SpecialnostiAdmin(admin.ModelAdmin):
    list_display = ('kod_specialnosti', 'nazvanie_specialnosti')

@admin.register(SpecialnostiGruppy)
class SpecialnostiGruppyAdmin(admin.ModelAdmin):
    list_display = ('nazvanie_gruppy', 'specialnosti_kod')

@admin.register(UchebnyjPlan)
class UchebnyjPlanAdmin(admin.ModelAdmin):
    list_display = ('nomer_modulya', 'naimenovanie_modulya', 'kompetencii')

@admin.register(ProfessionalnyeModuli)
class ProfessionalnyeModuliAdmin(admin.ModelAdmin):
    list_display = ('nomer_mdk', 'naimenovanie_mdk', 'modul_nomer')

@admin.register(Praktiki)
class PraktikiAdmin(admin.ModelAdmin):
    list_display = ('nomer_praktiki', 'period_nomer', 'specialnost_kod', 'modul_nomer')

@admin.register(RukovoditeliPraktik)
class RukovoditeliPraktikAdmin(admin.ModelAdmin):
    list_display = ('praktika_nomer', 'rukovoditel_nomer')

@admin.register(Zadaniya)
class ZadaniyaAdmin(admin.ModelAdmin):
    list_display = ('nomer_zadaniya', 'nazvanie_temy', 'vidy_rabot', 'kolichestvo_chasov_na_odnu_rabotu', 'praktika_nomer')