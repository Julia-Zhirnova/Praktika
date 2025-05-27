# main/models.py
'''
from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta

class Sezon(models.Model):
    kod_sezona = models.AutoField(db_column='Kod_sezona', primary_key=True)
    naimenovanie_sezona = models.CharField(db_column='Naimenovanie_sezona', max_length=10, unique=True)

    def __str__(self):
        return self.naimenovanie_sezona

class Tip(models.Model):
    kod_tipa = models.CharField(db_column='Kod_tipa', max_length=10, primary_key=True)
    naimenovanie_tipa = models.CharField(db_column='Naimenovanie_tipa', max_length=50, unique=True)

    def __str__(self):
        return self.naimenovanie_tipa

class PeriodyPraktiki(models.Model):
    nomer_perioda = models.AutoField(db_column='Nomer_perioda', primary_key=True)
    sezon_kod = models.ForeignKey('Sezon', models.DO_NOTHING, db_column='Sezon_kod')
    god = models.IntegerField(db_column='God')
    obem_v_chasah = models.SmallIntegerField(db_column='Obem_v_chasah')
    data_nachala = models.DateField(db_column='Data_nachala')
    data_vydachi_zadaniya = models.DateField(db_column='Data_vydachi_zadaniya', blank=True, null=True)
    data_okonchaniya = models.DateField(db_column='Data_okonchaniya')
    tip_kod = models.ForeignKey('Tip', models.DO_NOTHING, db_column='Tip_kod', blank=True, null=True)

    # def clean(self):
    #     # Валидация года
    #     if not (2000 <= self.god <= 2100):
    #         raise ValidationError({'god': 'Год должен быть между 2000 и 2100.'})

    #     # Валидация объема в часах
    #     if not (0 <= self.obem_v_chasah <= 200):
    #         raise ValidationError({'obem_v_chasah': 'Объем в часах должен быть между 0 и 200.'})

    #     # Автоматическое заполнение даты выдачи задания
    #     if self.tip_kod:
    #         if self.tip_kod.kod_tipa == '1':
    #             self.data_vydachi_zadaniya = self.data_nachala
    #         elif self.tip_kod.kod_tipa == '2':
    #             self.data_vydachi_zadaniya = self.data_nachala - timedelta(days=1)

    def __str__(self):
        return f"{self.sezon_kod} {self.god}"

    class Meta:
        verbose_name_plural = "Периоды практики"# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
'''

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    patronymic = models.CharField(max_length=150, blank=True, null=True, verbose_name="Отчество")

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic or ''}".strip()
    
from django.db import models

class Tip(models.Model):
    kod_tipa = models.CharField(db_column='Kod_tipa', primary_key=True)  # Field name made lowercase.
    naimenovanie_tipa = models.CharField(db_column='Naimenovanie_tipa', unique=True)  # Field name made lowercase.

    def __str__(self):
        return self.naimenovanie_tipa
    
    class Meta:
        managed = False
        db_table = 'Tip'

from django.db import models


class Sezon(models.Model):
    kod_sezona = models.AutoField(db_column='Kod_sezona', primary_key=True)  # Field name made lowercase.
    naimenovanie_sezona = models.CharField(db_column='Naimenovanie_sezona', unique=True)  # Field name made lowercase.

    def __str__(self):
        return self.naimenovanie_sezona
    
    class Meta:
        managed = False
        db_table = 'Sezon'
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class PeriodyPraktiki(models.Model):
    nomer_perioda = models.AutoField(db_column='Nomer_perioda', primary_key=True)  # Field name made lowercase.
    sezon_kod = models.ForeignKey('Sezon', models.DO_NOTHING, db_column='Sezon_kod')  # Field name made lowercase.
    god = models.IntegerField(db_column='God')  # Field name made lowercase.
    obem_v_chasah = models.SmallIntegerField(db_column='Obem_v_chasah')  # Field name made lowercase.
    data_nachala = models.DateField(db_column='Data_nachala')  # Field name made lowercase.
    data_vydachi_zadaniya = models.DateField(db_column='Data_vydachi_zadaniya', blank=True, null=True)  # Field name made lowercase.
    data_okonchaniya = models.DateField(db_column='Data_okonchaniya')  # Field name made lowercase.
    tip_kod = models.ForeignKey('Tip', models.DO_NOTHING, db_column='Tip_kod', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return f"{self.sezon_kod} {self.god}"
    
    class Meta:
        managed = False
        db_table = 'Periody_praktiki'
