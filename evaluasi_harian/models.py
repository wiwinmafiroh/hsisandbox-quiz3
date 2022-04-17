from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Peserta(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  nip = models.CharField(max_length=20, unique=True)
  nama_lengkap = models.CharField(max_length=100)
  alamat = models.TextField()
  tanggal_lahir = models.DateField()
  no_hp = models.CharField(max_length=15)
  
  def __str__(self):
    return self.nama_lengkap
  
  class Meta:
    verbose_name_plural = 'Peserta'

class LembarEvaluasi(models.Model):
  status = [
    ('Aktif', 'Aktif'),
    ('Tidak Aktif', 'Tidak Aktif'),
    ('Selesai', 'Selesai'),
  ]
  
  kode_evaluasi = models.CharField(max_length=10, unique=True)
  nama_evaluasi = models.CharField(max_length=100)
  jumlah_soal = models.IntegerField(default=2)
  skor = models.IntegerField(default=4)
  status = models.CharField(max_length=20, choices=status, default='Tidak Aktif')
  
  def __str__(self):
    return self.kode_evaluasi
  
  class Meta:
    verbose_name_plural = 'Lembar Evaluasi'

class BankSoal(models.Model):
  opsi = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
  ]
  
  lembar_evaluasi = models.ForeignKey(LembarEvaluasi, on_delete=models.CASCADE)
  soal = models.TextField()
  pilihan_a = models.CharField(max_length=200)
  pilihan_b = models.CharField(max_length=200)
  pilihan_c = models.CharField(max_length=200)
  pilihan_d = models.CharField(max_length=200)
  kunci_jawaban = models.CharField(max_length=1, choices=opsi)
  
  def __str__(self):
    return self.soal
  
  class Meta:
    verbose_name_plural = 'Bank Soal'

class HasilEvaluasi(models.Model):
  peserta = models.ForeignKey(Peserta, on_delete=models.CASCADE)
  lembar_evaluasi = models.ForeignKey(LembarEvaluasi, on_delete=models.CASCADE)
  bank_soal = models.ForeignKey(BankSoal, on_delete=models.CASCADE)
  jawaban = models.CharField(max_length=1)
  is_true = models.BooleanField()
  skor = models.IntegerField(default=0)
  waktu_pengerjaan = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return "{} - {}".format(self.peserta, self.jawaban)
  
  class Meta:
    verbose_name_plural = 'Hasil Evaluasi'
    
class NilaiEvaluasi(models.Model):
  peserta = models.ForeignKey(Peserta, on_delete=models.CASCADE)
  lembar_evaluasi = models.ForeignKey(LembarEvaluasi, on_delete=models.CASCADE)
  total_skor = models.IntegerField(null=True)
  total_nilai_evaluasi = models.FloatField(null=True, default=0)
  
  def __str__(self):
    return "{} - {}".format(self.peserta, self.total_nilai_evaluasi)
  
  class Meta:
    verbose_name_plural = 'Nilai Evaluasi'

class NilaiAkhir(models.Model):
  predikat = [
    ('Mumtaz Murtafi', 'Mumtaz Murtafi'),
    ('Mumtaz', 'Mumtaz'),
    ('Jayyid Jiddan', 'Jayyid Jiddan'),
    ('Jayyid', 'Jayyid'),
    ('Maqbul', 'Maqbul'),
    ('Rasib', 'Rasib'),
    ('Ghayyib', 'Ghayyib'),
  ]
  peserta = models.ForeignKey(Peserta, on_delete=models.CASCADE)
  nilai_akhir = models.FloatField(null=True, default=0)
  predikat = models.CharField(max_length=50, choices=predikat, default='Ghayyib')
  
  def __str__(self):
    return "{} - {} - {}".format(self.peserta, self.nilai_akhir, self.predikat)
  
  class Meta:
    verbose_name_plural = 'Nilai Akhir'
  
  