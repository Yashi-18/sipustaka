from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="""

            CREATE TABLE IF NOT EXISTS siswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama VARCHAR(100),
                kelas VARCHAR(20),
                nis VARCHAR(50) UNIQUE,
                is_active BOOLEAN
            );

            CREATE TABLE IF NOT EXISTS buku (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul VARCHAR(150),
                pengarang VARCHAR(100),
                stok INTEGER,
                tahun_terbit INTEGER,
                kategori VARCHAR(100),
                penerbit VARCHAR(100),
                rak VARCHAR(100),
                deskripsi TEXT
            );

            CREATE TABLE IF NOT EXISTS peminjaman (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                siswa_id INTEGER,
                buku_id INTEGER,
                tanggal_pinjam DATE,
                jatuh_tempo DATE,
                keperluan TEXT,
                status VARCHAR(50),
                keterangan TEXT,
                petugas VARCHAR(100),

                FOREIGN KEY (siswa_id)
                    REFERENCES siswa(id),

                FOREIGN KEY (buku_id)
                    REFERENCES buku(id)
            );

            CREATE INDEX IF NOT EXISTS idx_peminjaman_siswa
                ON peminjaman(siswa_id);

            CREATE INDEX IF NOT EXISTS idx_peminjaman_buku
                ON peminjaman(buku_id);

            """,

            reverse_sql="""

            DROP TABLE IF EXISTS peminjaman;
            DROP TABLE IF EXISTS buku;
            DROP TABLE IF EXISTS siswa;

            """
        )
    ]