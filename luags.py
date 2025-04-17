import tkinter as tk 
from tkinter import messagebox, ttk
import sqlite3

connect = sqlite3.connect("expenses.db")
c = connect.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, amount REAL, category TEXT)''')
connect.commit()

window = tk.Tk()
window.geometry("400x400")
window.title("Izdevumu pārvaldnieks")
window.resizable(False, False)

frame = tk.Frame(window, padx=10, pady=10)
frame.pack()

title = tk.Label(frame, text="Izdevumu pārvaldnieks", font=("Helvetica", 16, "bold"))
title.grid(row=0, column=0, columnspan=2, pady=(0, 15))


tk.Label(frame, text="Summa (€):", font=("Helvetica", 16, "bold")).grid(row=1, column=0, sticky="e")
amountt = tk.Entry(frame, width=20)
amountt.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Kategorija:", font=("Helvetica", 16, "bold")).grid(row=2, column=0, sticky="e")
categoryy = ttk.Combobox(frame, values=["Ēdiens", "Sabiedriskā dzīve", "Mājdzīvnieki", "Transports", "Kultūra", "Mājsaimniecība", "Apģērbs", "Skaistumkopšana", "Veselība", "Mācības", "Dāvana", "Cits"], width = 20)
categoryy.grid(row=2, column=1, pady=5)

frame3 = tk.Frame(window, padx=10, pady=10)
frame3.pack()

output = tk.Text(frame3, height=12, width=45, bg="#f9f9f9", borderwidth=1, relief="solid")
output.pack()

def add():
    try:
        amount = float(amountt.get())
        category = categoryy.get()
        if category == "":
            raise ValueError
        with connect:
            connect.execute("INSERT INTO expenses (amount, category) VALUES (?, ?)", (amount, category))
        messagebox.showinfo("Izdevums veiksmīgi pievienots!")
        amountt.delete(0, tk.END)
        categoryy.delete(0,tk.END)
        show()
    except ValueError:
        messagebox.showerror("Nepareiza ievade! Lūdzu ievadiet pareizu summu un kategoriju")

def show():
    output.delete(1.0, tk.END)
    rows = connect.execute("SELECT amount, category FROM expenses").fetchall()
    total = 0
    for row in rows:
        output.insert(tk.END, f"{row[0]:.2f} € - {row[1]}\n")
        total += row[0]
    output.insert(tk.END, f"\nKopā: {total:.2f} €")

frame2 = tk.Frame(window, pady=10)
frame2.pack()

#a

tk.Button(frame2, text = "Pievienot izdevumu", command=add, bg="#4CAF50", fg="white", padx=10).grid(row=0, column=0, padx=5)
tk.Button(frame2, text= "Apskatīt visus izdevumus", command=show, bg="#2196F3", fg="white", padx=10).grid(row=0, column=1, padx=5)




window.mainloop()