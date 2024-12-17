import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi membuat database dan tabel
def create_database():
    conn = sqlite3.connect('data_karyawan.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS karyawan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            alamat TEXT NOT NULL,
            posisi TEXT NOT NULL,
            tahun_bergabung INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('data_karyawan.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM karyawan')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Menyimpan data ke database
def save_to_database(nama, alamat, posisi, tahun):
    conn = sqlite3.connect('data_karyawan.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO karyawan (nama, alamat, posisi, tahun_bergabung)
        VALUES (?, ?, ?, ?)
    ''', (nama, alamat, posisi, tahun))
    conn.commit()
    conn.close()

# Mengupdate data di database
def update_database(record_id, nama, alamat, posisi, tahun):
    conn = sqlite3.connect('data_karyawan.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE karyawan
        SET nama = ?, alamat = ?, posisi = ?, tahun_bergabung = ?
        WHERE id = ?
    ''', (nama, alamat, posisi, tahun, record_id))
    conn.commit()
    conn.close()

# Menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('data_karyawan.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM karyawan WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Fungsi tombol submit
def submit():
    try:
        nama = nama_var.get()
        alamat = alamat_var.get()
        posisi = posisi_var.get()
        tahun = int(tahun_var.get())

        if not nama or not alamat or not posisi or not tahun:
            raise ValueError("Semua field harus diisi!")
        
        save_to_database(nama, alamat, posisi, tahun)
        messagebox.showinfo("Sukses", "Data karyawan berhasil disimpan!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi tombol update
def update():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk di-update.")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        alamat = alamat_var.get()
        posisi = posisi_var.get()
        tahun = int(tahun_var.get())

        if not nama or not alamat or not posisi or not tahun:
            raise ValueError("Semua field harus diisi!")
        
        update_database(record_id, nama, alamat, posisi, tahun)
        messagebox.showinfo("Sukses", "Data karyawan berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi tombol delete
def delete():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data karyawan berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Membersihkan input form
def clear_inputs():
    nama_var.set("")
    alamat_var.set("")
    posisi_var.set("")
    tahun_var.set("")
    selected_record_id.set("")

# Menampilkan data di tabel
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)

# Mengisi input form ketika memilih data dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        alamat_var.set(selected_row[2])
        posisi_var.set(selected_row[3])
        tahun_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# GUI
root = Tk()
root.title("Data Karyawan")

# Variabel input
nama_var = StringVar()
alamat_var = StringVar()
posisi_var = StringVar()
tahun_var = StringVar()
selected_record_id = StringVar()

# Label dan Entry
Label(root, text="Nama").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Alamat").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=alamat_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Posisi").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=posisi_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Tahun Bergabung").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=tahun_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol CRUD
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ('id', 'nama', 'alamat', 'posisi', 'tahun_bergabung')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Memuat data awal
populate_table()

root.mainloop()
