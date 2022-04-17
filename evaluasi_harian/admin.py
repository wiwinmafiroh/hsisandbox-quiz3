from django.contrib import admin
from .models import *

# Register your models here.
class PesertaDisplay(admin.ModelAdmin):
  list_display = ('nip', 'nama_lengkap')

class LembarEvaluasiDisplay(admin.ModelAdmin):
  list_display = ('kode_evaluasi', 'nama_evaluasi', 'status')
  
class BankSoalDisplay(admin.ModelAdmin):
  list_display = ('lembar_evaluasi', 'soal', 'pilihan_a', 'pilihan_b', 'pilihan_c', 'pilihan_d', 'kunci_jawaban')
  
class HasilEvaluasiDisplay(admin.ModelAdmin):
  list_display = ('id', 'peserta', 'lembar_evaluasi', 'bank_soal', 'jawaban', 'skor')

class NilaiDisplay(admin.ModelAdmin):
  list_display = ('peserta', 'lembar_evaluasi', 'total_nilai_evaluasi', 'total_skor')
  
class NilaiAkhirDisplay(admin.ModelAdmin):
  list_display = ('peserta', 'nilai_akhir', 'predikat')
  
admin.site.register(Peserta, PesertaDisplay)
admin.site.register(LembarEvaluasi, LembarEvaluasiDisplay)
admin.site.register(BankSoal, BankSoalDisplay)
admin.site.register(HasilEvaluasi, HasilEvaluasiDisplay)
admin.site.register(NilaiEvaluasi, NilaiDisplay)
admin.site.register(NilaiAkhir, NilaiAkhirDisplay)