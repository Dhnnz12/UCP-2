import sqlite3
import tkinter as tk
from tkinter import messagebox

# Membuat tabel data_kompetisi
def initialize_db():
    conn = sqlite3.connect("data_kompetisi.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_kompetisi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            asal_kampus TEXT,
            prodi TEXT,
            semester INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Fungsi untuk menyimpan data ke database
def submit_data():
    nama = entry_nama.get()
    asal_kampus = entry_asal_kampus.get()
    prodi = entry_prodi.get()
    
    # Validasi input semester
    try:
        semester = int(entry_semester.get())
        if semester <= 0:
            messagebox.showerror("Error", "Semester harus berupa angka positif.")
            return
    except ValueError:
        messagebox.showerror("Error", "Masukkan semester berupa angka.")
        return

    # Menyimpan data ke database
    conn = sqlite3.connect("data_kompetisi.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO data_kompetisi (nama, asal_kampus, prodi, semester)
        VALUES (?, ?, ?, ?)
    """, (nama, asal_kampus, prodi, semester))
    conn.commit()
    conn.close()

    # Tampilkan pesan sukses
    messagebox.showinfo("Sukses", "Data kompetisi telah disimpan.")

    # Mengosongkan field input
    entry_nama.delete(0, tk.END)
    entry_asal_kampus.delete(0, tk.END)
    entry_prodi.delete(0, tk.END)
    entry_semester.delete(0, tk.END)

# Inisialisasi database
initialize_db()

# Membuat GUI menggunakan Tkinter
root = tk.Tk()
root.title("Data Kompetisi")

# Label dan Entry untuk nama
tk.Label(root, text="Nama:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nama = tk.Entry(root, width=30)
entry_nama.grid(row=0, column=1, padx=10, pady=5)

# Label dan Entry untuk asal kampus
tk.Label(root, text="Asal Kampus:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_asal_kampus = tk.Entry(root, width=30)
entry_asal_kampus.grid(row=1, column=1, padx=10, pady=5)

# Label dan Entry untuk prodi
tk.Label(root, text="Prodi:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_prodi = tk.Entry(root, width=30)
entry_prodi.grid(row=2, column=1, padx=10, pady=5)

# Label dan Entry untuk semester
tk.Label(root, text="Semester:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_semester = tk.Entry(root, width=30)
entry_semester.grid(row=3, column=1, padx=10, pady=5)

# Button untuk submit data
btn_submit = tk.Button(root, text="Submit Data", command=submit_data, width=20, bg="lightblue")
btn_submit.grid(row=4, column=0, columnspan=2, pady=10)

# Menjalankan GUI
root.mainloop()