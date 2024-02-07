import tkinter as tk
import home.Homepage as Homepage
import MalkhanaTable.checkout.checkoutpage as cof
import MalkhanaTable.MalkhanaPage as m
import Log.log as log
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
import datetime
import logger as lu
import login.login as login
checkout_frame = None


def update_item_status(barcode):
    con = sqlite3.connect('databases/items_in_malkhana.db')
    cursor = con.cursor()
    cursor.execute(
        "UPDATE items SET item_status='FSL' where barcode = ?", (barcode,))
    con.commit()
    con.close()


def checkout_destroyer():
    if checkout_frame is not None:
        checkout_frame.destroy()


def checkouttoFSL():
    barcode = barcode_entry.get()
    fir_no = fir_no_entry.get()
    seized_items = seized_items_entry.get()
    taken_by_whom = taken_by_whom_entry.get()
    checkout_date = checkout_date_entry.get_date()
    checkout_time = f"{hour_var.get()}:{minute_var.get()}"
    order_no = order_no_entry.get()

    barcode_checker(barcode, checkout_date, checkout_time, taken_by_whom,
                    seized_items, fir_no, order_no)


def checkouttoFSL_page(root):
    root.destroy()
    global checkout_frame, barcode_entry, fir_no_entry, seized_items_entry, taken_by_whom_entry, checkout_date_entry, hour_var, minute_var, order_no_entry
    checkout_destroyer()
    checkout_frame = tk.Frame(root.master)
    checkout_frame.master.title("Check Out to FSL")
    checkout_frame.pack()

    # Labels
    label_barcode = ttk.Label(
        checkout_frame, text="Barcode:",  background="#B9E6FF", font=("Helvetica", 12))
    label_fir_no = ttk.Label(
        checkout_frame, text="FIR No:", background="#B9E6FF", font=("Helvetica", 12))
    label_item_name = ttk.Label(
        checkout_frame, text="Seized Items:",  background="#B9E6FF", font=("Helvetica", 12))
    label_taken_by_whom = ttk.Label(
        checkout_frame, text="Undertaking Inspector:", background="#B9E6FF", font=("Helvetica", 12))
    label_checkout_date = ttk.Label(
        checkout_frame, text="Checkout Date:", background="#B9E6FF", font=("Helvetica", 12))
    label_checkout_time = ttk.Label(
        checkout_frame, text="Checkout Time:",  background="#B9E6FF", font=("Helvetica", 12))
    label_order_no = ttk.Label(
        checkout_frame, text="Order No:", background="#B9E6FF", font=("Helvetica", 12))

    label_barcode.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    label_fir_no.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    label_item_name.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    label_taken_by_whom.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    label_checkout_date.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
    label_checkout_time.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
    label_order_no.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

    # Entry fields
    barcode_entry = ttk.Entry(checkout_frame, font=("Helvetica", 12))
    fir_no_entry = ttk.Entry(checkout_frame, font=("Helvetica", 12))
    seized_items_entry = ttk.Entry(checkout_frame, font=("Helvetica", 12))
    taken_by_whom_entry = ttk.Entry(checkout_frame, font=("Helvetica", 12))
    order_no_entry = ttk.Entry(checkout_frame, font=("Helvetica", 12))
    barcode_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    fir_no_entry    .grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    seized_items_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    taken_by_whom_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    order_no_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    hour_var = tk.StringVar(checkout_frame, value='00')
    minute_var = tk.StringVar(checkout_frame, value='00')

    hour_menu = ttk.Combobox(checkout_frame, textvariable=hour_var, values=[
                             str(i).zfill(2) for i in range(24)], state='readonly', width=5)
    minute_menu = ttk.Combobox(checkout_frame, textvariable=minute_var, values=[
                               str(i).zfill(2) for i in range(60)], state='readonly', width=5)
    hour_menu.grid(row=6, column=1, padx=0, pady=5, sticky=tk.W)
    minute_menu.grid(row=6, column=2, padx=0, pady=5, sticky=tk.W)

    # Date field using tkcalendar
    checkout_date_entry = DateEntry(
        checkout_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    checkout_date_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

    # Checkout button
    checkout_button = tk.Button(checkout_frame, text="FSL ને ચેકઆઉટ",
                                background="#FFFFFF", command=checkouttoFSL, font=("Helvetica", 12))
    checkout_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

    # Home and Back buttons
    home_button = tk.Button(checkout_frame, text="હોમપેજ",
                            background="#FFFFFF", command=go_home, font=("Helvetica", 12))
    home_button.grid(row=9, column=0, padx=10, pady=10, sticky=tk.E)

    back_button = tk.Button(checkout_frame, text="પાછા જાઓ",
                            background="#FFFFFF", command=go_back, font=("Helvetica", 12))
    back_button.grid(row=9, column=1, padx=10, pady=10, sticky=tk.W)


def go_back():
    checkout_destroyer()
    m.mkpage(checkout_frame)


def go_home():
    checkout_destroyer()
    Homepage.open_homepage_r(checkout_frame)


def barcode_checker(barcode, date, time, taken_by_whom, seized_items, fir_no, order_no):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchall()
    conn.close()

    if not result:
        messagebox.showerror("Barcode Not Found!",
                             "Barcode doesnt exist in database.")
        # Clear the input fields after showing the error
        barcode_entry.delete(0, tk.END)
        fir_no_entry.delete(0, tk.END)
        seized_items_entry.delete(0, tk.END)
        taken_by_whom_entry.delete(0, tk.END)
        checkout_date_entry.set_date(None)  # Clear the date entry
        order_no_entry.delete(0, tk.END)
        return
    already_outornot(barcode, date, time, taken_by_whom,
                     seized_items, fir_no, order_no)
    # Clear the input fields after successful checkout
    barcode_entry.delete(0, tk.END)
    fir_no_entry.delete(0, tk.END)
    seized_items_entry.delete(0, tk.END)
    taken_by_whom_entry.delete(0, tk.END)
    checkout_date_entry.set_date(None)  # Clear the date entry
    order_no_entry.delete(0, tk.END)


def already_outornot(barcode, date, time, taken_by_whom, seized_items, fir_no, order_no):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_status FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] in ("malkhana", "Malkhana"):
        update_item_status(barcode)
        log.update_logs(barcode, "FSLમાં ચેકઆઉટ કર્યું", date, time)
        messagebox.showinfo("સફળતા", "મુદ્દામાલ સફળતાથી FSL માં મોકલ્યો છે!")
        addfslpage(barcode, date, time, taken_by_whom,
                   seized_items, fir_no, order_no)
        activity = "Item checked out to FSL barcode no:"+barcode
        lu.log_activity(login.current_user, activity)
    else:
        messagebox.showerror("મુદ્દામાલ ઉપલબ્ધ નથી",
                             "મુદ્દામાલ માલખાનામાં ઉપલબ્ધ નથી.")
        barcode_entry.delete(0, tk.END)
        fir_no_entry.delete(0, tk.END)

        seized_items_entry.delete(0, tk.END)
        taken_by_whom_entry.delete(0, tk.END)
        checkout_date_entry.set_date(None)
        order_no_entry.delete(0, tk.END)


def addfslpage(barcode, date, time, taken_by_whom, seized_items, fir_no, order_no):
    conn = sqlite3.connect("databases/fsl_records.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS fsl_records (
    barcode TEXT UNIQUE,
    fir_no TEXT UNIQUE,
    seized_items TEXT,
    order_no INTEGER UNIQUE,
    checkout_date TEXT,
    checkout_time TEXT,
    taken_by_whom TEXT,
    checkin_date TEXT,
    checkin_time TEXT,
    examiner_name TEXT,
    fsl_report TEXT,
    entry_time TEXT
    );''')
    entry_time = datetime.datetime.now()
    cursor.execute("INSERT INTO fsl_records (barcode,fir_number,item_name,order_no,checkout_date,checkout_time,taken_by_whom,entry_time) values(?,?,?,?,?,?,?,?)",
                   (barcode, fir_no, seized_items, order_no, date, time, taken_by_whom, entry_time))
    conn.commit()
    conn.close()