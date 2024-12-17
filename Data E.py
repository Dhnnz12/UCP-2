import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

def create_database():
    conn = sqlite3.connect('makanan.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS makanan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_makanan TEXT NOT NULL,
        bahan TEXT,
        kandungan_nutrisi TEXT,
        jumlah_kalori INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def fetch_data():
    conn = sqlite3.connect('makanan.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM makanan')
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_to_database(nama, bahan, nutrisi, kalori):
    conn = sqlite3.connect('makanan.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO makanan (nama_makanan, bahan, kandungan_nutrisi, jumlah_kalori)
        VALUES (?, ?, ?, ?)
    ''', (nama, bahan, nutrisi, kalori))
    conn.commit()
    conn.close()

def update_database(record_id, nama, bahan, nutrisi, kalori):
    conn = sqlite3.connect('makanan.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE makanan
        SET nama_makanan = ?, bahan = ?, kandungan_nutrisi = ?, jumlah_kalori = ?
        WHERE id = ?
    ''', (nama, bahan, nutrisi, kalori, record_id))
    conn.commit()
    conn.close()

def delete_database(record_id):
    conn = sqlite3.connect('makanan.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM makanan WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

def submit():
    try:
        nama = nama_var.get()
        bahan = bahan_var.get()
        nutrisi = nutrisi_var.get()
        kalori = int(kalori_var.get())

        if not nama:
            raise ValueError("Nama makanan tidak boleh kosong.")
        
        save_to_database(nama, bahan, nutrisi, kalori)
        messagebox.showinfo("Sukses", "Data Makanan Berhasil disimpan!")
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
        bahan = bahan_var.get()
        nutrisi = nutrisi_var.get()
        kalori = int(kalori_var.get())

        if not nama:
            raise ValueError("Nama makanan tidak boleh kosong.")
        
        update_database(record_id, nama, bahan, nutrisi, kalori)
        messagebox.showinfo("Sukses", "Data Makanan Berhasil diperbarui!")
        clear_inputs()
        populate_table()

    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data Makanan Berhasil dihapus!")
        clear_inputs()
        populate_table()

    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def clear_inputs():
    nama_var.set("")
    bahan_var.set("")
    nutrisi_var.set("")
    kalori_var.set("")
    selected_record_id.set("")

def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)

def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        bahan_var.set(selected_row[2])
        nutrisi_var.set(selected_row[3])
        kalori_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid")

create_database()

root = Tk()
root.title("Manajemen Data Makanan")

nama_var = StringVar()
bahan_var = StringVar()
nutrisi_var = StringVar()
kalori_var = StringVar()
selected_record_id = StringVar()

# Labels and Inputs
Label(root, text="Nama Makanan").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Bahan").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=bahan_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Kandungan Nutrisi").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=nutrisi_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Jumlah Kalori").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=kalori_var).grid(row=3, column=1, padx=10, pady=5)

# Buttons
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Table
columns = ('id', 'nama_makanan', 'bahan', 'kandungan_nutrisi', 'jumlah_kalori')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.replace('_', ' ').capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table()

root.mainloop()
