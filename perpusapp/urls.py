
from django.urls import path
from perpustakaan import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('buku/', views.buku_list, name='buku_list'),
    path('buku/tambah/', views.buku_tambah, name='buku_tambah'),
    path('buku/edit/<int:id>/', views.buku_edit, name='buku_edit'),
    path('buku/detail/<int:id>/', views.buku_detail, name='buku_detail'),
    path('buku/hapus/<int:id>/', views.buku_hapus, name='buku_hapus'),
    
    path('siswa/', views.siswa_list, name='siswa_list'),
    path('siswa/tambah/', views.siswa_tambah, name='siswa_tambah'),
    path('siswa/edit/<int:id>/', views.siswa_edit, name='siswa_edit'),
    path('siswa/detail/<int:id>/', views.siswa_detail, name='siswa_detail'),
    path('siswa/hapus/<int:id>/', views.siswa_hapus, name='siswa_hapus'),
    
    path('peminjaman/', views.peminjaman_list, name='peminjaman_list'),
    path('peminjaman/tambah/', views.peminjaman_tambah, name='peminjaman_tambah'),
    path('peminjaman/ubah-status/<int:id>/', views.ubah_status_peminjaman, name='ubah_status_peminjaman'),
]