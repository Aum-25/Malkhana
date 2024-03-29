import tkinter as tk
from PIL import Image,ImageTk
from ttkthemes import ThemedStyle
import MalkhanaTable.additems.additems as a
import home.Homepage as Homepage
import MalkhanaTable.checkin.checkinpage as cp
import Log.log as log
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
import logger as lu
import login.login as login

fsl_checkin_frame = None


def update_item_status(barcode, checkin_date, checkin_time,
                       order_no, examiner, examiner_report):
    con = sqlite3.connect('databases/items_in_malkhana.db')
    cursor = con.cursor()
    cursor.execute(
        "UPDATE items SET item_status='malkhana' where barcode = ?", (barcode,))
    con.commit()
    con.close()
    conn = sqlite3.connect("databases/fsl_records.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE fsl_records SET checkin_date = ?,checkin_time=?,examiner_name=?,fsl_report = ? WHERE order_no = ?",
                   (checkin_date, checkin_time, examiner, examiner_report, order_no))
    barcode_entry.delete(0, tk.END)
    examiner_entry.delete(0, tk.END)
    checkin_date_entry.set_date(None)
    order_no_entry.delete(0, tk.END)
    examiner_report_entry.delete("1.0", tk.END)
    conn.commit()
    conn.close()
    messagebox.showinfo("Successful", "Succesfully entered into Malkhana")
    log.update_logs(barcode, "Checkin From FSL",
                    checkin_date, checkin_time)
    activity = "Item checked in from FSL barcode no: "+barcode
    lu.log_activity(login.current_user, activity)

def set_custom_theme(root):
    # Load and display background image
    bg_image = Image.open("bg.jpeg")
    # Resize the image to match the window size
    bg_image = bg_image.resize((root.winfo_screenwidth(), 1000), Image.LANCZOS)

    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
def checkin():
    barcode = barcode_entry.get()
    checkin_time = f"{hour_var.get()}:{minute_var.get()}"
    checkin_date = checkin_date_entry.get_date()
    order_no = order_no_entry.get()
    examiner = examiner_entry.get()
    examiner_report = examiner_report_entry.get("1.0", "end-1c")

    barcode_checker(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report)


def checkin_page(prev_checkin_page):
    global fsl_checkin_frame, barcode_entry, order_no_entry, checkin_date_entry, hour_var, minute_var, examiner_report_entry, examiner_entry
    fsL_checkin_destroyer()
    fsl_checkin_frame = tk.Frame(prev_checkin_page.master)
    fsl_checkin_frame.master.title("Checkin From FSL")

     # Get screen width and height
    screen_width = fsl_checkin_frame.winfo_screenwidth()
    screen_height = fsl_checkin_frame.winfo_screenheight()

    # Load and resize background image
    bg_image = Image.open("bg.jpeg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(fsl_checkin_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Use pack for the fsl_checkin_frame
    fsl_checkin_frame.pack(fill=tk.BOTH, expand=True)
    style = ThemedStyle(fsl_checkin_frame)
    style.theme_use('radiance')

    # Labels
    label_barcode_no = tk.Label(
        fsl_checkin_frame, text="Barcode No:",  background="#fff1f1", font=("Helvetica", 12))
    label_order_no = tk.Label(
        fsl_checkin_frame, text="Order No:",   background="#fff1f1", font=("Helvetica", 12))
    label_checkin_time = tk.Label(
        fsl_checkin_frame, text="Checkin Time:",  background="#fff1f1", font=("Helvetica", 12))
    label_checkin_date = tk.Label(
        fsl_checkin_frame, text="Checkin Date:", background="#fff1f1", font=("Helvetica", 12))
    label_examiner = tk.Label(
        fsl_checkin_frame, text="Examiner Name:",   background="#fff1f1", font=("Helvetica", 12))
    label_examiner_report = tk.Label(
        fsl_checkin_frame, text="Examiner Report:",   background="#fff1f1", font=("Helvetica", 12))

    label_barcode_no.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    label_order_no.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    label_checkin_time.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
    label_checkin_date.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
    label_examiner.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
    label_examiner_report.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)

    # Entry fields
    barcode_entry = ttk.Entry(
        fsl_checkin_frame, width=30, font=("Helvetica", 12))
    # Use sticky=tk.W for left alignment
    barcode_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
    order_no_entry = ttk.Entry(
        fsl_checkin_frame, width=30, font=("Helvetica", 12))
    order_no_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    hour_var = tk.StringVar(fsl_checkin_frame, value='00')
    minute_var = tk.StringVar(fsl_checkin_frame, value='00')

    hour_menu = ttk.Combobox(fsl_checkin_frame, textvariable=hour_var, values=[
                             str(i).zfill(2) for i in range(24)], state='readonly', width=5)
    minute_menu = ttk.Combobox(fsl_checkin_frame, textvariable=minute_var, values=[
                               str(i).zfill(2) for i in range(60)], state='readonly', width=5)
    hour_menu.grid(row=2,  column=1, padx=10, pady=10, sticky="w")
    minute_menu.grid(row=2,  column=1, padx=(10, 150), pady=10, sticky="e")

    # Date field using tkcalendar
    checkin_date_entry = DateEntry(
        fsl_checkin_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
    # Use sticky=tk.W for left alignment
    checkin_date_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

    examiner_entry = ttk.Entry(
        fsl_checkin_frame,  background="#FFFFFF", font=("Helvetica", 12))
    examiner_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

    # Text area for examiner report
    examiner_report_entry = tk.Text(
        fsl_checkin_frame, height=5, background="#FFFFFF", width=30, font=("Helvetica", 12))
    # Use sticky=tk.W for left alignment
    examiner_report_entry.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)

    # Check-in button
    checkin_button = tk.Button(fsl_checkin_frame, text="Checkin",
                               background="#9a9a9a", command=checkin, font=("Helvetica", 12))
    checkin_button.grid(row=6, column=0, columnspan=4,
                        padx=10, pady=10, sticky="ew")

    button_font = ('Helvetica', 12)
    back_button = tk.Button(fsl_checkin_frame, text="Back",
                            background="#9a9a9a", command=go_back, font=button_font)
    back_button.grid(row=0, column=30, padx=10, pady=10, sticky="w")

    home_button = tk.Button(fsl_checkin_frame, text="Home",
                            background="#9a9a9a", command=go_home, font=button_font)
    home_button.grid(row=0, column=31, padx=10, pady=10, sticky="w")


def go_home():
    fsL_checkin_destroyer()
    Homepage.open_homepage(fsl_checkin_frame)


def go_back():
    fsL_checkin_destroyer()
    cp.CIpage(fsl_checkin_frame)


def fsL_checkin_destroyer():
    if fsl_checkin_frame is not None:
        fsl_checkin_frame.destroy()


def barcode_checker(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchall()
    conn.close()

    if not result:
        messagebox.showerror("Barcode Not Found",
                             "Entered Barcode Not Found In Database.")
        # Clear the input fields after showing the error
        barcode_entry.delete(0, tk.END)
        examiner_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)
        examiner_report_entry.delete("1.0", tk.END)
        return

    already_inornot(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report)
    # Clear the input fields after successful checkout
    barcode_entry.delete(0, tk.END)
    examiner_entry.delete(0, tk.END)
    checkin_date_entry.set_date(None)
    examiner_report_entry.delete("1.0", tk.END)


def already_inornot(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_status FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] in ("fsl", "FSL"):
        update_item_status(barcode, checkin_date, checkin_time,
                           order_no, examiner, examiner_report)

    else:
        messagebox.showerror("Item Exists In Malkhana/Court",
                             "Item Already Exists In Malkhana/Court.")
        barcode_entry.delete(0, tk.END)
        examiner_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)
        examiner_report_entry.delete("1.0", tk.END)
