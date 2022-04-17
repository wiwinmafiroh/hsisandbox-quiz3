from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    
    path('adminhsi/', views.adminhsi, name='adminhsi'),
    path('adminhsi/lembar_evaluasi/', views.lembar_evaluasi, name='lembar_evaluasi'),
    path('adminhsi/add_evaluasi/', views.add_evaluasi, name='add_evaluasi'),
    path('adminhsi/edit_evaluasi/<int:id>/', views.edit_evaluasi, name='edit_evaluasi'),
    path('adminhsi/pilih_evaluasi/', views.pilih_evaluasi, name='pilih_evaluasi'),
    path('adminhsi/soal_evaluasi/<int:id>/', views.soal_evaluasi, name='soal_evaluasi'),
    path('adminhsi/add_soal/<int:id>/', views.add_soal, name='add_soal'),
    path('adminhsi/edit_soal/<int:id>/', views.edit_soal, name='edit_soal'),
    path('adminhsi/delete_soal/<int:id>/', views.delete_soal, name='delete_soal'),
    path('adminhsi/nilai/', views.nilai_peserta, name='nilai_peserta'),
    
    path('pesertahsi/', views.pesertahsi, name='pesertahsi'),
    path('pesertahsi/confirm/', views.evaluasi_confirm, name='evaluasi_confirm'),
    path('pesertahsi/evaluasi/', views.evaluasi_start, name='evaluasi_start'),
    path('pesertahsi/hasil/', views.evaluasi_hasil, name='evaluasi_hasil'),
    path('pesertahsi/arsip/', views.arsip, name='arsip'),
    path('pesertahsi/peringkat/', views.peringkat, name='peringkat'),
]
