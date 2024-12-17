import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# 1. Create or update database schema
def create_database():
    conn = sqlite3.connect('nilai_mata_kuliah.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nilai_mata_kuliah (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        kode_mata_kuliah TEXT NOT NULL,
        kelas TEXT NOT NULL,
        nilai INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# 2. Fetch all records
def fetch_data():
    conn = sqlite3.connect('nilai_mata_kuliah.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nilai_mata_kuliah')
    rows = cursor.fetchall()
    conn.close()
    return rows

# 3. Save new record to database
def save_to_database(nama, kode_mk, kelas, nilai):
    conn = sqlite3.connect('nilai_mata_kuliah.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_mata_kuliah (nama_siswa, kode_mata_kuliah, kelas, nilai)
        VALUES (?, ?, ?, ?)
    ''', (nama, kode_mk, kelas, nilai))
    conn.commit()
    conn.close()

# 4. Update existing record
def update_database(record_id, nama, kode_mk, kelas, nilai):
    conn = sqlite3.connect('nilai_mata_kuliah.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_mata_kuliah
        SET nama_siswa = ?, kode_mata_kuliah = ?, kelas = ?, nilai = ?
        WHERE id = ?
    ''', (nama, kode_mk, kelas, nilai, record_id))
    conn.commit()
    conn.close()

# 5. Delete a record
def delete_database(record_id):
    conn = sqlite3.connect('nilai_mata_kuliah.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_mata_kuliah WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# 6. Handle submit action
def submit():
    try:
        nama = nama_var.get()
        kode_mk = kode_mk_var.get()
        kelas = kelas_var.get()
        nilai = int(nilai_var.get())

        if not nama or not kode_mk or not kelas:
            raise ValueError("Semua field harus diisi!")

        save_to_database(nama, kode_mk, kelas, nilai)
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# 7. Handle update action
def update():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk di-update.")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        kode_mk = kode_mk_var.get()
        kelas = kelas_var.get()
        nilai = int(nilai_var.get())

        if not nama or not kode_mk or not kelas:
            raise ValueError("Semua field harus diisi!")
        
        update_database(record_id, nama, kode_mk, kelas, nilai)
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# 8. Handle delete action
def delete():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# 9. Clear input fields
def clear_inputs():
    nama_var.set("")
    kode_mk_var.set("")
    kelas_var.set("")
    nilai_var.set("")
    selected_record_id.set("")

# 10. Populate Treeview
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)

# 11. Fill inputs from table selection
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        kode_mk_var.set(selected_row[2])
        kelas_var.set(selected_row[3])
        nilai_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid")

# GUI Configuration
create_database()
root = Tk()
root.title("Input Nilai Mata Kuliah")

# Variables
nama_var = StringVar()
kode_mk_var = StringVar()
kelas_var = StringVar()
nilai_var = StringVar()
selected_record_id = StringVar()

# Input Fields
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Kode Mata Kuliah").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=kode_mk_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Kelas").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=kelas_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=nilai_var).grid(row=3, column=1, padx=10, pady=5)

# Buttons
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Treeview Table
columns = ('id', 'nama_siswa', 'kode_mata_kuliah', 'kelas', 'nilai')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.replace("_", " ").capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table()
root.mainloop()
