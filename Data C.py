import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Database Setup
def create_database():
    conn = sqlite3.connect('iuran_rutin.db')
    cursor = conn.cursor()
    # Table for Iuran Rutin
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS iuran_rutin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        bulan TEXT NOT NULL,
        tahun INTEGER NOT NULL,
        nominal INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Database Operations
def fetch_iuran_data():
    conn = sqlite3.connect('iuran_rutin.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM iuran_rutin')
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_iuran_to_database(nama, bulan, tahun, nominal):
    conn = sqlite3.connect('iuran_rutin.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO iuran_rutin (nama, bulan, tahun, nominal)
        VALUES (?, ?, ?, ?)
    ''', (nama, bulan, tahun, nominal))
    conn.commit()
    conn.close()

def update_iuran_database(record_id, nama, bulan, tahun, nominal):
    conn = sqlite3.connect('iuran_rutin.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE iuran_rutin
        SET nama = ?, bulan = ?, tahun = ?, nominal = ?
        WHERE id = ?
    ''', (nama, bulan, tahun, nominal, record_id))
    conn.commit()
    conn.close()

def delete_iuran_database(record_id):
    conn = sqlite3.connect('iuran_rutin.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM iuran_rutin WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Functions
def submit():
    try:
        nama = nama_var.get()
        bulan = bulan_var.get()
        tahun = int(tahun_var.get())
        nominal = int(nominal_var.get())

        if not nama or not bulan:
            raise ValueError("Nama dan Bulan tidak boleh kosong.")
        
        save_iuran_to_database(nama, bulan, tahun, nominal)
        messagebox.showinfo("Sukses", "Data Iuran Berhasil Disimpan!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

def update():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk di-update.")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        bulan = bulan_var.get()
        tahun = int(tahun_var.get())
        nominal = int(nominal_var.get())

        if not nama or not bulan:
            raise ValueError("Nama dan Bulan tidak boleh kosong.")
        
        update_iuran_database(record_id, nama, bulan, tahun, nominal)
        messagebox.showinfo("Sukses", "Data Iuran Berhasil Diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_iuran_database(record_id)
        messagebox.showinfo("Sukses", "Data Iuran Berhasil Dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def clear_inputs():
    nama_var.set("")
    bulan_var.set("")
    tahun_var.set("")
    nominal_var.set("")
    selected_record_id.set("")

def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_iuran_data():
        tree.insert('', 'end', values=row)

def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        bulan_var.set(selected_row[2])
        tahun_var.set(selected_row[3])
        nominal_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid")

# GUI Setup
create_database()
root = Tk()
root.title("Data Iuran Rutin")

# Variables
nama_var = StringVar()
bulan_var = StringVar()
tahun_var = StringVar()
nominal_var = StringVar()
selected_record_id = StringVar()

# Labels and Entry Widgets
Label(root, text="Nama").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Bulan").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=bulan_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Tahun").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=tahun_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nominal").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=nominal_var).grid(row=3, column=1, padx=10, pady=5)

# Buttons
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Table
columns = ('id', 'nama', 'bulan', 'tahun', 'nominal')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table()
root.mainloop()
