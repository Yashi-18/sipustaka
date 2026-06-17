from django.shortcuts import render, redirect
from django.db import connection

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dashboard(request):
    with connection.cursor() as cursor:
        # 1. Hitung Total Buku (SUM dari kolom stok)
        cursor.execute("SELECT SUM(stok) FROM buku")
        total_buku = cursor.fetchone()[0] or 0

        # 2. Hitung Total Judul (Jumlah baris di tabel buku)
        cursor.execute("SELECT COUNT(*) FROM buku")
        total_judul = cursor.fetchone()[0] or 0

        # 3. Hitung Sedang Dipinjam
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dipinjam'")
        total_dipinjam = cursor.fetchone()[0] or 0

        # 4. Hitung Sudah Dikembalikan
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dikembalikan'")
        total_kembali = cursor.fetchone()[0] or 0

        # 5. Ambil data buku untuk progress bar (Analisis Stok)
        # Gunakan dictfetchall agar bisa dipanggil dengan nama kolom (b.judul)
        cursor.execute("SELECT judul, stok FROM buku LIMIT 5")
        columns = [col[0] for col in cursor.description]
        buku = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'total_dipinjam': total_dipinjam,
        'total_kembali': total_kembali,
        'buku': buku,
    }
    return render(request, 'dashboard.html', context)

# --- 2. MODUL BUKU ---
def buku_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku ORDER BY id DESC")
        buku = dictfetchall(cursor)
    return render(request, 'buku_list.html', {'buku': buku})

def buku_tambah(request):
    if request.method == 'POST':
        p = request.POST
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO buku (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                [p.get('judul'), p.get('pengarang'), p.get('kategori'), p.get('penerbit'), p.get('tahun_terbit'), p.get('rak'), p.get('stok'), p.get('deskripsi')]
            )
        return redirect('buku_list')
    return render(request, 'buku_form.html')

def buku_edit(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            p = request.POST
            cursor.execute(
                "UPDATE buku SET judul=%s, pengarang=%s, kategori=%s, penerbit=%s, tahun_terbit=%s, rak=%s, stok=%s, deskripsi=%s WHERE id=%s",
                [p.get('judul'), p.get('pengarang'), p.get('kategori'), p.get('penerbit'), p.get('tahun_terbit'), p.get('rak'), p.get('stok'), p.get('deskripsi'), id]
            )
            return redirect('buku_list')
        cursor.execute("SELECT * FROM buku WHERE id = %s", [id])
        buku = dictfetchall(cursor)[0]
    return render(request, 'buku_form.html', {'buku': buku})

def buku_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku WHERE id = %s", [id])
        buku = dictfetchall(cursor)[0]
    return render(request, 'buku_detail.html', {'buku': buku})

def buku_hapus(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM buku WHERE id = %s", [id])
    return redirect('buku_list')

# --- 3. MODUL SISWA ---
def siswa_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa ORDER BY id DESC")
        siswa = dictfetchall(cursor)
    return render(request, 'siswa_list.html', {'siswa': siswa})

def siswa_tambah(request):
    if request.method == 'POST':
        p = request.POST
        is_active = True if p.get('is_active') == 'True' else False
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO siswa (nama, kelas, nis, is_active) VALUES (%s, %s, %s, %s)",
                [p.get('nama'), p.get('kelas'), p.get('nis'), is_active]
            )
        return redirect('siswa_list')
    return render(request, 'siswa_form.html')

def siswa_edit(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            p = request.POST
            is_active = True if p.get('is_active') == 'True' else False
            cursor.execute(
                "UPDATE siswa SET nama=%s, kelas=%s, nis=%s, is_active=%s WHERE id=%s",
                [p.get('nama'), p.get('kelas'), p.get('nis'), is_active, id]
            )
            return redirect('siswa_list')
        cursor.execute("SELECT * FROM siswa WHERE id = %s", [id])
        siswa = dictfetchall(cursor)[0]
    return render(request, 'siswa_form.html', {'siswa': siswa})

def siswa_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa WHERE id = %s", [id])
        siswa = dictfetchall(cursor)[0]
    return render(request, 'siswa_detail.html', {'siswa': siswa})

def siswa_hapus(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM siswa WHERE id = %s", [id])
    return redirect('siswa_list')

# --- 4. MODUL PEMINJAMAN ---
def peminjaman_list(request):
    with connection.cursor() as cursor:
        # PERHATIKAN: Ganti 'siswa_id' atau 'id_siswa' sesuai nama kolom asli di tabel peminjaman kamu
        query = """
            SELECT p.id, s.nama AS nama_siswa, b.judul AS judul_buku, 
                   p.tanggal_pinjam, p.jatuh_tempo, p.status,
                   p.keperluan, p.petugas
            FROM peminjaman p
            JOIN siswa s ON p.siswa_id = s.id
            JOIN buku b ON p.buku_id = b.id
            ORDER BY p.id DESC
        """
        try:
            cursor.execute(query)
            rows = dictfetchall(cursor)
        except Exception as e:
            # Jika error id_siswa, coba jalankan query dengan nama 'siswa_id'
            # Ini hanya untuk jaga-jaga kalau nama kolom di DB beda
            return render(request, 'error.html', {'pesan': str(e)})

    return render(request, 'peminjaman_list.html', {'peminjaman': rows})

def peminjaman_tambah(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            p = request.POST
            cursor.execute(
                "INSERT INTO peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status) VALUES (%s, %s, %s, %s, %s, %s)",
                [p.get('siswa_id'), p.get('buku_id'), p.get('tanggal_pinjam'), p.get('jatuh_tempo'), p.get('keperluan'), p.get('status')]
            )
            return redirect('peminjaman_list')
        
        cursor.execute("SELECT id, nama FROM siswa WHERE is_active = True")
        siswa = dictfetchall(cursor)
        cursor.execute("SELECT id, judul FROM buku WHERE stok > 0")
        buku = dictfetchall(cursor)
        
    return render(request, 'peminjaman_form.html', {'siswa': siswa, 'buku': buku})

def ubah_status_peminjaman(request, id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE peminjaman SET status = 'Dikembalikan' WHERE id = %s", [id])
    return redirect('peminjaman_list')