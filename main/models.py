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

from django.db import models


class Specialnosti(models.Model):
    kod_specialnosti = models.CharField(db_column='Kod_specialnosti', primary_key=True)  # Field name made lowercase.
    nazvanie_specialnosti = models.CharField(db_column='Nazvanie_specialnosti', unique=True)  # Field name made lowercase.

    def __str__(self):
        return self.nazvanie_specialnosti
    
    class Meta:
        managed = False
        db_table = 'Specialnosti'

from django.db import models


class SpecialnostiGruppy(models.Model):
    nazvanie_gruppy = models.CharField(db_column='Nazvanie_gruppy', primary_key=True)  # Field name made lowercase.
    specialnosti_kod = models.ForeignKey('Specialnosti', models.DO_NOTHING, db_column='Specialnosti_kod')  # Field name made lowercase.

    def __str__(self):
        return f"{self.specialnosti_kod}"
    
    class Meta:
        managed = False
        db_table = 'Specialnosti_Gruppy'

class UchebnyjPlan(models.Model):
    nomer_modulya = models.CharField(db_column='Nomer_modulya', primary_key=True, max_length=10)
    naimenovanie_modulya = models.CharField(db_column='Naimenovanie_modulya', unique=True, max_length=255)
    kompetencii = models.TextField(db_column='Kompetencii')

    class Meta:
        managed = False
        db_table = 'Uchebnyj_plan'

class ProfessionalnyeModuli(models.Model):
    nomer_mdk = models.CharField(db_column='Nomer_MDK', primary_key=True, max_length=10)
    naimenovanie_mdk = models.CharField(db_column='Naimenovanie_MDK', max_length=255)
    modul_nomer = models.ForeignKey(UchebnyjPlan, models.DO_NOTHING, 
                   db_column='Modul_nomer', to_field='nomer_modulya')

    class Meta:
        managed = False
        db_table = 'Professionalnye_moduli'
        
class Praktiki(models.Model):
    nomer_praktiki = models.AutoField(db_column='Nomer_praktiki', primary_key=True)
    period_nomer = models.ForeignKey(
        'PeriodyPraktiki',
        on_delete=models.DO_NOTHING,  # Explicit on_delete argument
        db_column='Period_nomer'
    )
    specialnost_kod = models.ForeignKey(
        'Specialnosti',
        on_delete=models.DO_NOTHING,  # Explicit on_delete argument
        db_column='Specialnost_kod'
    )
    modul_nomer = models.ForeignKey(
        'UchebnyjPlan',  # Ссылка на модель UchebnyjPlan
        on_delete=models.DO_NOTHING,
        db_column='Modul_nomer',
        to_field='nomer_modulya'  # Поле, на которое ссылается ForeignKey
    )

    class Meta:
        managed = False
        db_table = 'Praktiki'


from django.db import models


class Zadaniya(models.Model):
    nomer_zadaniya = models.CharField(db_column='Nomer_zadaniya', primary_key=True)  # Field name made lowercase.
    nazvanie_temy = models.TextField(db_column='Nazvanie_temy')  # Field name made lowercase.
    vidy_rabot = models.TextField(db_column='Vidy_rabot')  # Field name made lowercase.
    kolichestvo_chasov_na_odnu_rabotu = models.SmallIntegerField(db_column='Kolichestvo_chasov_na_odnu_rabotu')  # Field name made lowercase.
    praktika_nomer = models.ForeignKey('Praktiki', models.DO_NOTHING, db_column='Praktika_nomer')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Zadaniya'

from django.db import models

class RukovoditeliPraktik(models.Model):
    praktika_nomer = models.ForeignKey(
        Praktiki,
        on_delete=models.DO_NOTHING,
        db_column='Praktika_nomer',
        related_name='rukovoditeli'
    )
    rukovoditel_nomer = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        db_column='Rukovoditel_nomer'
    )
    nomer_rukovoditeli_praktik = models.AutoField(
        primary_key=True,
        db_column='Nomer_rukovoditeli_praktik'
    )

    class Meta:
        managed = False
        db_table = 'Rukovoditeli_praktik'