import tkinter as tk 
from tkinter import messagebox, ttk
import sqlite3

connect = sqlite3.connect("expenses.db")
c = connect.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, amount REAL, category TEXT)''')
connect.commit()

window = tk.Tk()
window.geometry("560x530")
window.title("Izdevumu pārvaldnieks")
window.resizable(False, False)
window.configure(bg="#dbe2ea")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 10), padding=6)
style.map("TButton", background=[("active", "#e0e0e0")])

frame = tk.Frame(window, bg="#dbe2ea", padx=20, pady=10)
frame.pack()

title = tk.Label(frame, text="Izdevumu pārvaldnieks", font=("Helvetica", 18, "bold"), bg="#dbe2ea", fg="#2e3f53")
title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

tk.Label(frame, text="Summa (€):", font=("Helvetica", 12), bg="#dbe2ea", fg="#2e3f53").grid(row=1, column=0, sticky="e")
amountt = tk.Entry(frame, width=24, font=("Helvetica", 10) )
amountt.grid(row=1, column=1, pady=5)

tk.Label(frame, text="(izmanto punktu, nevis komatu: piem. 5.50)", font=("Helvetica", 8), bg="#dbe2ea", fg="gray").grid(row=2, column=1, sticky="w")

tk.Label(frame, text="Kategorija:", font=("Helvetica", 12), bg="#dbe2ea", fg="#2e3f53").grid(row=3, column=0, sticky="e")
categoryy = ttk.Combobox(frame, values=[
    "Ēdiens", "Sabiedriskā dzīve", "Mājdzīvnieki", "Transports",
    "Kultūra", "Mājsaimniecība", "Apģērbs", "Skaistumkopšana",
    "Veselība", "Mācības", "Dāvana", "Cits"
], width=22)
categoryy.grid(row=3, column=1, pady=5)

frame2 = tk.Frame(window, pady=10, bg="#dbe2ea")
frame2.pack()

button_width = 20

def style_button(widget, bg, fg):
    widget.configure(bg=bg, fg=fg, activebackground="#d0d0d0", relief="flat", bd=1, font=("Helvetica", 10, "bold"))

status_label = tk.Label(frame2, text="", font=("Helvetica", 10), fg="green")
status_label.grid(row=1, column=0, columnspan=2, pady=5)

frame3 = tk.Frame(window, padx=10, pady=10, bg="#dbe2ea")
frame3.pack()

output = tk.Text(frame3, height=12, width=60, bg="#ffffff", borderwidth=1, relief="groove", font=("Courier", 10))
output.pack()

def add():
    try:
        amount = float(amountt.get())
        category = categoryy.get()
        if category == "":
            raise ValueError
        with connect:
            connect.execute("INSERT INTO expenses (amount, category) VALUES (?, ?)", (amount, category))
        status_label.config(text="Izdevums veiksmīgi pievienots!", fg="green")
        amountt.delete(0, tk.END)
        categoryy.set("")
    except ValueError:
        status_label.config(text="Nepareiza ievade! Izmanto punktu kā decimālzīmi un izvēlies kategoriju!", fg="red")

def show():
    output.delete(1.0, tk.END)
    rows = connect.execute("SELECT id, amount, category FROM expenses").fetchall()
    total = 0
    for row in rows:
        output.insert(tk.END, f"ID {row[0]:<3} | {row[1]:>6.2f} € | {row[2]}\n")
        total += row[1]
    output.insert(tk.END, f"\n{'-'*40}\nKopā: {total:.2f} €")

def delete_last():
    with connect:
        last = connect.execute("SELECT id FROM expenses ORDER BY id DESC LIMIT 1").fetchone()
        if last:
            connect.execute("DELETE FROM expenses WHERE id=?", (last[0],))
            status_label.config(text="Pēdējais izdevums izdzēsts!", fg="blue")
            show()
        else:
            status_label.config(text="Nav ko dzēst!", fg="orange")
        
def delete_all():
    confirm = messagebox.askyesno("Apstiprināt", "Vai tiešām vēlies dzēst visus izdevumus?")
    if confirm:
        with connect:
            connect.execute("DELETE FROM expenses")
        status_label.config(text="Visi izdevumi ir izdzēsti.", fg="darkred")
        show()

btn_add = tk.Button(frame2, text="Pievienot izdevumu", width = button_width, command=add)
style_button(btn_add, "#4CAF50", "white")
btn_add.grid(row=0, column=0, padx=6, pady=5)

btn_show = tk.Button(frame2, text="Apskatīt visus izdevumus", width = button_width, command=show)
style_button(btn_show, "#2196F3", "white")
btn_show.grid(row=0, column=1, padx=6, pady=5)

btn_del = tk.Button(frame2, text="Dzēst pēdējo ierakstu", width = button_width, command=delete_last)
style_button(btn_del, "#f44336", "white")
btn_del.grid(row=0, column=2, padx=6, pady=5)

btn_del_all = tk.Button(frame2, text="Dzēst visus", width=button_width, command=delete_all)
style_button(btn_del_all, "#9E9E9E", "white")
btn_del_all.grid(row=1, column=1, padx=6, pady=5)

status_frame = tk.Frame(window, bg="#dbe2ea")
status_frame.pack()
status_label = tk.Label(status_frame, text="", font=("Helvetica", 10), bg="#dbe2ea", fg="green")
status_label.pack(pady=5)

window.mainloop()
