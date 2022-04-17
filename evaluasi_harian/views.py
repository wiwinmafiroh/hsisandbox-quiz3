from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .forms import LoginForm
from .models import *

import random

# Create your views here.
### LOGIN ###
def loginView(request):
  form = LoginForm()
  
  if request.method == 'POST':
    username = request.POST['username'].lower()
    password = request.POST['password']
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
      login(request, user)
      if user.groups.filter(name='admin'):
        return redirect('adminhsi')
      else:
        return redirect('pesertahsi')
    else:
      messages.error(request, 'Username atau Password Salah!')
      return redirect('login')
  
  context = {
    'form': form,
  }
  return render(request, 'login/login.html', context)

### LOGOUT ###
@login_required(login_url='login')
def logoutView(request):
  logout(request)
  return redirect('login')





### ADMIN ###
# Admin
@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def adminhsi(request):
  jml_peserta = Peserta.objects.count()
  jml_lembar_evaluasi = LembarEvaluasi.objects.count()
  jml_bank_soal = BankSoal.objects.count()
  
  context = {
    'jml_peserta': jml_peserta,
    'jml_lembar_evaluasi': jml_lembar_evaluasi,
    'jml_bank_soal': jml_bank_soal,
  }
  return render(request, 'adminhsi/dashboard.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def lembar_evaluasi(request):
  lembar_evaluasi = LembarEvaluasi.objects.all()
  
  context = {
    'lembar_evaluasi': lembar_evaluasi,
  }
  return render(request, 'adminhsi/lembar_evaluasi.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def add_evaluasi(request):
  # Generate kode evaluasi
  inisial_kode = 'EH0'
  kode_terakhir = LembarEvaluasi.objects.last()
  kode_baru = inisial_kode + str(int(kode_terakhir.kode_evaluasi[2:]) + 1) 
  
  # Cek dan ambil data dari form
  if request.method == 'POST':
    kode_evaluasi = request.POST['kode_evaluasi']
    nama_evaluasi = request.POST['nama_evaluasi']
    status = request.POST['status']
    
    # Cek apakah masih ada evaluasi yang akif
    evaluasi_aktif = LembarEvaluasi.objects.filter(status='Aktif')
    
    if evaluasi_aktif.count() > 0 and status == 'Aktif':
      messages.warning(request, 'Masih Ada Evaluasi yang Aktif!')
      return redirect('add_evaluasi')
  
    # Simpan data
    lembar_evaluasi = LembarEvaluasi(kode_evaluasi=kode_evaluasi, nama_evaluasi=nama_evaluasi, status=status)
    lembar_evaluasi.save()
    messages.success(request, 'Data Evaluasi Berhasil Ditambahkan!')
    return redirect('lembar_evaluasi') 
  
  context = {
    'kode_baru': kode_baru,
  }
  return render(request, 'adminhsi/add_evaluasi.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def edit_evaluasi(request, id):
  lembar_evaluasi = LembarEvaluasi.objects.get(id=id)
  
  # Cek dan ambil data dari form
  if request.method == 'POST':
    kode_evaluasi = request.POST['kode_evaluasi']
    nama_evaluasi = request.POST['nama_evaluasi']
    status = request.POST['status']
    
    # Cek apakah masih ada evaluasi yang akif
    data_evaluasi = LembarEvaluasi.objects.filter()
    evaluasi_aktif = data_evaluasi.filter(status='Aktif')
    
    # Jika ada evaluasi yang aktif dan status lama evaluasi bukan aktif
    if evaluasi_aktif.count() > 0 and status == 'Aktif' and lembar_evaluasi.status != 'Aktif':
      messages.warning(request, 'Masih Ada Evaluasi yang Aktif!')
      return redirect('edit_evaluasi', id)
  
    # Simpan data
    lembar_evaluasi.kode_evaluasi = kode_evaluasi
    lembar_evaluasi.nama_evaluasi = nama_evaluasi
    lembar_evaluasi.status = status
    lembar_evaluasi.save()
    messages.success(request, 'Data Evaluasi Berhasil Diubah!')
    return redirect('lembar_evaluasi') 
  
  context = {
    'lembar_evaluasi': lembar_evaluasi,
  }
  return render(request, 'adminhsi/edit_evaluasi.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def pilih_evaluasi(request):
  list_evaluasi = LembarEvaluasi.objects.all()
  
  context = {
    'list_evaluasi': list_evaluasi,
  }
  return render(request, 'adminhsi/pilih_evaluasi.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def soal_evaluasi(request, id):
  # Ambil data lembar evaluasi berdasarkan id yang dikirim
  evaluasi = LembarEvaluasi.objects.get(id=id) 
  kode_evaluasi = evaluasi.kode_evaluasi
  
  bank_soal = BankSoal.objects.filter(lembar_evaluasi=evaluasi).order_by('-id')
  jml_soal = bank_soal.count()
  
  context = {
    'id': id,
    'evaluasi': evaluasi,
    'kode_evaluasi': kode_evaluasi,
    'bank_soal': bank_soal,
    'jml_soal': jml_soal,
  }
  return render(request, 'adminhsi/soal_evaluasi.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def add_soal(request, id):
  evaluasi = LembarEvaluasi.objects.get(id=id)
  bank_soal = BankSoal.objects.filter(lembar_evaluasi=evaluasi) 
  
  # Cek dan ambil data dari form
  if request.method == 'POST':
    soal = request.POST['soal']
    pilihan_a = request.POST['pilihan_a']
    pilihan_b = request.POST['pilihan_b']
    pilihan_c = request.POST['pilihan_c']
    pilihan_d = request.POST['pilihan_d']
    kunci_jawaban = request.POST['kunci_jawaban']
    
    # Simpan data
    bank_soal = BankSoal(soal=soal, pilihan_a=pilihan_a, pilihan_b=pilihan_b, pilihan_c=pilihan_c, pilihan_d=pilihan_d, kunci_jawaban=kunci_jawaban, lembar_evaluasi=evaluasi)
    bank_soal.save()
    messages.success(request, 'Soal Berhasil Ditambahkan!')
    return redirect('soal_evaluasi', id) 
  
  context = {
    'id': id,
    'evaluasi': evaluasi,
  }
  return render(request, 'adminhsi/add_soal.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def edit_soal(request, id):
  # Ambil data bank soal berdasarkan id
  bank_soal = BankSoal.objects.get(id=id)
  
  # Ambil id lembar evaluasi dari bank soal
  id_evaluasi = bank_soal.lembar_evaluasi.id
  
  # Mengambil data
  if request.method == 'POST':
    soal = request.POST['soal']
    pilihan_a = request.POST['pilihan_a']
    pilihan_b = request.POST['pilihan_b']
    pilihan_c = request.POST['pilihan_c']
    pilihan_d = request.POST['pilihan_d']
    kunci_jawaban = request.POST['kunci_jawaban']
    
    # Simpan data
    bank_soal.soal = soal
    bank_soal.pilihan_a = pilihan_a
    bank_soal.pilihan_b = pilihan_b
    bank_soal.pilihan_c = pilihan_c
    bank_soal.pilihan_d = pilihan_d
    bank_soal.kunci_jawaban = kunci_jawaban
    bank_soal.save()
    messages.success(request, 'Soal Berhasil Diubah!')
    return redirect('soal_evaluasi', bank_soal.lembar_evaluasi.id) 
  
  context = {
    'id_evaluasi': id_evaluasi,
    'bank_soal': bank_soal,
  }
  return render(request, 'adminhsi/edit_soal.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def delete_soal(request, id):
  # Ambil data bank soal berdasarkan id
  bank_soal = BankSoal.objects.get(id=id)
  
  # Ambil id lembar evaluasi dari bank soal
  id_evaluasi = bank_soal.lembar_evaluasi.id
  
  # Hapus data
  bank_soal.delete()
  messages.success(request, 'Soal Berhasil Dihapus!')
  return redirect('soal_evaluasi', id_evaluasi)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='admin'), login_url='login')
def nilai_peserta(request):
  # Ambil data nilai akhir
  nilai_peserta = NilaiAkhir.objects.all().order_by('-nilai_akhir')
  
  context = {
    'nilai_peserta': nilai_peserta,
  }
  return render(request, 'adminhsi/nilai_peserta.html', context)





### PESERTA ###
@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='peserta'), login_url='login')
def pesertahsi(request):
  # Ambil data peserta yang login
  peserta = Peserta.objects.get(user=request.user)
  nama_lengkap = peserta.nama_lengkap
  nip = peserta.nip
  
  # Ambil lembar evaluasi yang aktif
  evaluasi_aktif = LembarEvaluasi.objects.filter(status='Aktif')
  kode_evaluasi = ''
  status_evaluasi = ''
  
  # Cek apakah ada lembar evaluasi yang aktif
  if evaluasi_aktif:
    kode_evaluasi = evaluasi_aktif[0].kode_evaluasi
    data_evaluasi = HasilEvaluasi.objects.filter(peserta=peserta, lembar_evaluasi__kode_evaluasi=kode_evaluasi)
    
    if data_evaluasi.count() == 0:
      status_evaluasi = 'Kerjakan'
    else:
      status_evaluasi = 'Selesai'
  else:
    status_evaluasi = 'Tidak Ada'
  
  context = {
    'nama_lengkap': nama_lengkap, 
    'nip': nip,
    'kode_evaluasi': kode_evaluasi,
    'status_evaluasi': status_evaluasi,
  }
  return render(request, 'pesertahsi/dashboard.html',  context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='peserta'), login_url='login')
def evaluasi_confirm(request):
  # Ambil data peserta yang login
  peserta = Peserta.objects.get(user=request.user)
  nama_lengkap = peserta.nama_lengkap
  nip = peserta.nip
  
  # Ambil lembar evaluasi yang aktif
  evaluasi_aktif = LembarEvaluasi.objects.filter(status='Aktif')
  kode_evaluasi = ''
  
  # Cek apakah ada lembar evaluasi yang aktif
  if evaluasi_aktif:
    kode_evaluasi = evaluasi_aktif[0].kode_evaluasi
    data_evaluasi = HasilEvaluasi.objects.filter(peserta=peserta, lembar_evaluasi__kode_evaluasi=kode_evaluasi)
    
    # Cek apakah peserta sudah pernah mengerjakan evaluasi tersebut atau belum
    if data_evaluasi.count() == 0:
      messages.warning(request, 'Evaluasi Sudah Aktif. Silahkan Kerjakan Evaluasi.')
    else:
      messages.info(request, 'Alhamdulillah, Evaluasi Sudah Dikerjakan.')
  else:
    messages.info(request, 'Belum Ada Evaluasi yang Aktif.')
    
  context = {
    'nama_lengkap': nama_lengkap,
    'nip': nip,
    'kode_evaluasi': kode_evaluasi,
  }
  return render(request, 'pesertahsi/evaluasi_confirm.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='peserta'), login_url='login')
def evaluasi_start(request):
  # Ambil data peserta yang login
  peserta = Peserta.objects.get(user=request.user)
  id_peserta = peserta.id
  nama_lengkap = peserta.nama_lengkap
  nip = peserta.nip
  
  # Ambil lembar evaluasi yang aktif
  evaluasi_aktif = LembarEvaluasi.objects.filter(status='Aktif')
  id_evaluasi = ''
  bank_soal_acak = ''
  
  # Cek apakah ada lembar evaluasi yang aktif
  if evaluasi_aktif: 
    id_evaluasi = evaluasi_aktif[0].id
    data_evaluasi = HasilEvaluasi.objects.filter(peserta=peserta, lembar_evaluasi__id=id_evaluasi)
    
    # Cek apakah peserta sudah pernah mengerjakan evaluasi tersebut atau belum
    if data_evaluasi.count() == 0:
      # Ambil bank soal berdasarkan lembar evaluasi yang aktif
      bank_soal = BankSoal.objects.filter(lembar_evaluasi__id=id_evaluasi)
      # ambil 2 soal acak dari bank_soal secara random
      bank_soal_acak = random.sample(list(bank_soal), 2) 
      
      # Cek apakah ada jawaban yang di kirim
      if request.method == 'POST':
        skor = 0
        total_skor = 0
        total_nilai_evaluasi = 0
        
        # Looping untuk mengambil data dari form (karena data yang dikirim ada 2 soal)
        for i in range(1, 3):    
          peserta = Peserta.objects.get(id=request.POST['id_peserta'+str(i)])
          lembar_evaluasi = LembarEvaluasi.objects.get(id=request.POST['id_evaluasi'+str(i)])
          bank_soal = BankSoal.objects.get(id=request.POST['id_soal'+str(i)])
          jawaban = request.POST['jawaban'+str(i)]
          
          # Cek apakah jawaban benar atau salah
          kunci_jawaban = bank_soal.kunci_jawaban
          if jawaban == kunci_jawaban:
            skor = 2;
            is_true = True
          else:
            skor = 1;
            is_true = False
            
          total_skor += skor
          
          # Simpan data ke hasil evaluasi
          hasil_evaluasi = HasilEvaluasi(
            peserta=peserta,
            lembar_evaluasi=lembar_evaluasi,
            bank_soal=bank_soal,
            jawaban=jawaban,
            is_true=is_true,
            skor=skor,
          )
          hasil_evaluasi.save()
        
        # Hitung total nilai evaluasi dari 2 soal per lembar evaluasi
        total_nilai_evaluasi = round(total_skor / 4 * 100, 1)
        nilai_evaluasi = NilaiEvaluasi(
          peserta=peserta,
          lembar_evaluasi=lembar_evaluasi,
          total_skor=total_skor,
          total_nilai_evaluasi=total_nilai_evaluasi,
        )
        nilai_evaluasi.save()
        
        # Ambil data nilai evaluasi & lembar evaluasi untuk menghitung nilai akhir dan predikatnya
        n_evaluasi = NilaiEvaluasi.objects.filter(peserta=peserta)
        t_lembar_evaluasi = LembarEvaluasi.objects.filter(status__in=['Aktif', 'Selesai']).count()
        t_nilai = 0
        for nilai in n_evaluasi:
          t_nilai += nilai.total_nilai_evaluasi
          nilai_akhir = round(t_nilai / t_lembar_evaluasi, 1)
        if nilai_akhir == 100:
          predikat = 'Mumtaz Murtafi'
        elif nilai_akhir >= 90:
          predikat = 'Mumtaz'
        elif nilai_akhir >= 80:
          predikat = 'Jayyid Jiddan'
        elif nilai_akhir >= 70:
          predikat = 'Jayyid'
        elif nilai_akhir >= 50:
          predikat = 'Maqbul'
        elif nilai_akhir >= 1:
          predikat = 'Rasib'
        else:
          predikat = 'Ghayyib'
        # Cek apakah ada data nilai akhir dari peserta yang login? Kalau tidak ada, simpan. Kalau ada, update data nilai akhir ke nilai yang baru.
        n_akhir_peserta = NilaiAkhir.objects.filter(peserta=peserta)
        if n_akhir_peserta.count() == 0:
          nilai_akhir_peserta = NilaiAkhir(
            peserta=peserta,
            nilai_akhir=nilai_akhir,
            predikat=predikat,
          )
          nilai_akhir_peserta.save()
        else:
          nilai_akhir_peserta = NilaiAkhir.objects.get(peserta=peserta)
          nilai_akhir_peserta.nilai_akhir = nilai_akhir
          nilai_akhir_peserta.predikat = predikat
          nilai_akhir_peserta.save()
        return redirect('evaluasi_hasil')
    else:
      return redirect('evaluasi_confirm')
  else:
    return redirect('evaluasi_confirm')
    
  context= {
    'id_peserta': id_peserta,
    'nama_lengkap': nama_lengkap,
    'nip': nip,
    'id_evaluasi': id_evaluasi,
    'bank_soal_acak': bank_soal_acak,
  }
  return render(request, 'pesertahsi/evaluasi_start.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='peserta'), login_url='login')
def evaluasi_hasil(request):
  # Ambil data peserta yang login
  peserta = Peserta.objects.get(user=request.user)
  nama_lengkap = peserta.nama_lengkap
  nip = peserta.nip
  
  # Ambil 2 id terakhir dari hasilevaluasi peserta yang login dan urutkan dari id terbesar
  hasil_evaluasi = HasilEvaluasi.objects.filter(peserta=peserta).order_by('-id')[:2]
  
  # Membalik urutan hasil evaluasi
  hasil_evaluasi = hasil_evaluasi[::-1] 
  
  # Ambil kode evaluasi
  kode_evaluasi = hasil_evaluasi[0].lembar_evaluasi.kode_evaluasi
  
  # Total kan skor dari hasil evaluasi terakhir
  total_skor = hasil_evaluasi[0].skor + hasil_evaluasi[1].skor
  
  context = {
    'nama_lengkap': nama_lengkap,
    'nip': nip,
    'hasil_evaluasi': hasil_evaluasi,
    'kode_evaluasi': kode_evaluasi,
    'total_skor': total_skor,
  }
  return render(request, 'pesertahsi/hasil_evaluasi.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='peserta'), login_url='login')
def arsip(request):
  # Ambil data peserta yang login
  peserta = Peserta.objects.get(user=request.user)
  nama_lengkap = peserta.nama_lengkap
  nip = peserta.nip
  
  lembar_evaluasi = LembarEvaluasi.objects.filter(status__in=['Aktif', 'Selesai'])
  hasil_evaluasi = HasilEvaluasi.objects.filter(peserta=peserta)
  nilai_evaluasi = NilaiEvaluasi.objects.filter(peserta=peserta)
  nilai_akhir = NilaiAkhir.objects.filter(peserta=peserta)
  
  # Hitung total skor peserta dari setiap lembar evaluasi
  total_skor_peserta = 0
  for nilai in nilai_evaluasi:
    total_skor_peserta += nilai.total_skor
  
  # Hitung total skor dari lembar evaluasi yang aktif dan selesai
  total_skor_evaluasi = 0
  for evaluasi in lembar_evaluasi:
    total_skor_evaluasi += evaluasi.skor
    
  # Predikat di nilai_akhir
  predikat = ''
  for predikat in nilai_akhir:
    predikat = predikat.predikat
      
  # Untuk setiap 2 hasil evaluasi yang ada di hasil_evaluasi
  list_evaluasi = []
  for i in range(0, len(hasil_evaluasi), 2):
    list_evaluasi.append(hasil_evaluasi[i:i+2])
    
  # Hitung skor untuk setiap 2 hasil evaluasi yang ada di list_evaluasi
  list_skor = []
  for i in range(0, len(list_evaluasi)):
    list_skor.append(list_evaluasi[i][0].skor + list_evaluasi[i][1].skor)
  
  # Masukkan list_skor kedalam list_evaluasi dalam bentuk object
  for i in range(0, len(list_evaluasi)):
    list_evaluasi[i][0].skor = list_skor[i]
    list_evaluasi[i][1].skor = list_skor[i]
  
  context = {
    'nama_lengkap': nama_lengkap,
    'nip': nip,
    'hasil_evaluasi': hasil_evaluasi,
    'nilai_evaluasi': nilai_evaluasi,
    'nilai_akhir': nilai_akhir,
    'total_skor_peserta': total_skor_peserta,
    'total_skor_evaluasi': total_skor_evaluasi,
    'predikat': predikat,
    'list_evaluasi': list_evaluasi,
  }
  return render(request, 'pesertahsi/arsip_evaluasi.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.groups.filter(name='peserta'), login_url='login')
def peringkat(request):
  # Ambil data peserta yang login
  peserta = Peserta.objects.get(user=request.user)
  nama_lengkap = peserta.nama_lengkap
  nip = peserta.nip
  
  # Ambil data nilai akhir
  nilai_peserta = NilaiAkhir.objects.all().order_by('-nilai_akhir')
  
  context = {
    'nama_lengkap': nama_lengkap,
    'nip': nip,
    'nilai_peserta': nilai_peserta,
  }
  return render(request, 'pesertahsi/peringkat.html', context)