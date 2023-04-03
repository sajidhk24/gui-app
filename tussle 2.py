import os
from datetime import datetime
from tkinter import *
from tkinter import messagebox, Radiobutton

from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from pyinvoice.templates import SimpleInvoice

root = Tk()
root.title('Tussle Enterprises')
myframe = Frame(root)
root.geometry('1100x700')

# root.overrideredirect(True)
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# root.attributes("-fullscreen", True)
# root.bind("<F11>", lambda event: root.attributes("-fullscreen",
#                                     not root.attributes("-fullscreen")))
# root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# root.overrideredirect(True)
# root.overrideredirect(False)
# root.attributes('-fullscreen',True)

bg_color = 'light blue'

# =====================variables===================
twoL = IntVar()
oneL = IntVar()
halfL = IntVar()
quaterL = IntVar()
small_quater = IntVar()

Total = IntVar()

c_one = StringVar()
c_two = StringVar()
c_half = StringVar()
c_quater = StringVar()
c_small_quater = StringVar()

total_cost = StringVar()

cname = StringVar()
pcode = StringVar()
add = StringVar()
State = StringVar()
city = StringVar()
contact = StringVar()
invoice = StringVar()
gateway = StringVar()
amount = StringVar()
email = StringVar()
tid = StringVar()

selected = IntVar()
due_amount = StringVar()

tcost = total_cost.get()


# ===========Function===============
def total():
    if oneL.get() == 0 and twoL.get() == 0 and quaterL.get() == 0 and halfL.get() == 0:
        messagebox.showerror('Error', 'Please select number of quantity')
    else:
        one = oneL.get()
        two = twoL.get()
        qter = quaterL.get()
        half = halfL.get()

        t = float(one * 190 + two * 205 + qter * 230 + half * 192)
        Total.set(one + two + qter + half)
        total_cost.set('Rs' + str(round(t, 2)))

        c_one.set('Rs: ' + str(round(one * 190, 2)))
        c_two.set('Rs: ' + str(round(two * 205, 2)))
        c_half.set('Rs: ' + str(round(half * 192, 2)))
        c_quater.set('Rs: ' + str(round(qter * 230, 2)))


def receipt():
    textarea.delete(1.0, END)
    # textarea.insert(END, "*" * 66, " \n")
    textarea.insert(END, "\t \t Tussle Enterprises \n".title())
    # textarea.insert(END, "*" * 66, " \n")
    textarea.insert(END, ' Items\tQuantity of Items\t  Cost of Items\n')
    textarea.insert(END, f'\nBailey [1L]\t\t{oneL.get()}\t  {c_one.get()}')
    textarea.insert(END, f'\n\nBailly [2L]\t\t{twoL.get()}\t  {c_two.get()}')
    textarea.insert(END, f'\n\nBailey [500ML]\t\t{halfL.get()}\t  {c_half.get()}')
    textarea.insert(END, f'\n\nBailey [250ML]\t\t{quaterL.get()}\t  {c_quater.get()}')
    textarea.insert(END, f"\n\n================================")
    textarea.insert(END, f'\nTotal Price\t\t{Total.get()}\t{total_cost.get()}')
    textarea.insert(END, f"\n================================")


def printout():
    if invoice.get() == "Invoice Number" or cname.get() == "Name/Company":
        messagebox.showerror('Error', 'Please enter Invoice Number or Name ')

    if selected.get() == 1:
        if not os.path.exists("Paid_Receipts"):
            os.makedirs("Paid_Receipts")
        doc = SimpleInvoice(f'Paid_Receipts/{invoice.get()}{cname.get()}.pdf')
    else:
        if not os.path.exists("Receipts"):
            os.makedirs("Receipts")
        doc = SimpleInvoice(f'Receipts/{invoice.get()}{cname.get()}.pdf')

    # Paid stamp, optional
    if selected.get() == 1:
        doc.is_paid = True
    else:
        doc.is_paid = False
    doc.invoice_info = InvoiceInfo(f"{invoice.get()}", datetime.now(), datetime.now())  # Invoice info, optional

    # Service Provider Info, optional
    doc.service_provider_info = ServiceProviderInfo(
        name='Tussle Enterprises',
        street='Shop No-17, Jagat Trade Center, Frazer Road',
        city='Patna',
        state='Bihar',
        country='India',
        post_code='800001',
        vat_tax_number='10ACRPZ2833K1Z6'
    )

    # Client info, optional
    # if contact.get() == "Contact Number":
    #     # messagebox.showwarning("Incomplete details")
    #     messagebox.showerror('Error', 'Please enter Contact Number')

    doc.client_info = ClientInfo(name=f"{cname.get().upper()}", email=f'{email.get()} | Phone No: {contact.get()}',
                                 street=f'{add.get()}'.title(),
                                 state=f'{state.get()}'.title(), post_code=f'{pcode.get()}')

    # Add Item
    item = [1, 2, 500, 250]
    # item = {"Bailey [1L]":{190}, "Bailey [2L]": {205}, "Bailey [500ML]":{230}, "Bailey [250ML]":{192}}
    for i in item:

        one = oneL.get()
        two = twoL.get()
        qter = quaterL.get()
        half = halfL.get()

        name = ''
        rs = 0
        count = 0
        if i == 1:
            rs += 190
            name += "Bailey [1L]"
            count += one
        elif i == 2:
            name += "Bailey [2L]"
            rs += 205
            count += two
        elif i == 500:
            name += "Bailey [500ML]"
            rs += 192
            count += half
        elif i == 250:
            name = "Bailey [250ML]"
            rs += 230
            count += qter
        doc.add_item(Item("Water", f"{name}", f"{count}", f"{rs}"))

    # Tax rate, optional
    # doc.set_item_tax_rate(20)  # 20%

    # Transactions detail, optional
    if selected.get() == 1 or selected.get() == 2:
        if gateway.get() == "OFFLINE" or "offline" or "Offline":
            gateway.set("CASH")
        if tid.get() == "Transaction-ID":
            tid.set("--xxxxxxx--")
    if selected.get() == 1 or selected.get() == 2:
        if doc.is_paid:
            doc.add_transaction(
                Transaction(f'{gateway.get().upper()}', f'{tid.get()}', datetime.now(), f'{total_cost.get()}'))
        else:
            # messagebox.showerror('Error', 'Please enter Gateway and Transection ID')
            doc.add_transaction(
                Transaction(f'{gateway.get().upper()}', f'{tid.get()}', datetime.now(), f"{amount.get()}"))

    # Optional
    doc.set_bottom_tip(
        f"Previous Dues RS:- {due_amount.get()} <br />"
        "Email: example@example.com<br />Don't hesitate to contact us for any questions.<br />Phone No:- +91 "
        "6200482915/960618018")

    doc.finish()


def reset():
    textarea.delete(1.0, END)
    oneL.set(0)
    twoL.set(0)
    halfL.set(0)
    quaterL.set(0)
    cname.set("Name/Company")
    add.set("Address")
    State.set("State")
    pcode.set("Postal-Code")
    email.set("Email @gmail.com")
    contact.set("Contact Number")
    gateway.set("Offline")
    amount.set("Receive-Pay")
    invoice.set("Invoice Number")
    tid.set("Transaction-ID")
    due_amount.set("No-Dues")
    selected.set(3)

    Total.set(0)

    c_one.set('')
    c_two.set('')
    c_half.set('')
    c_quater.set('')

    total_cost.set('')


def exit():
    if messagebox.askyesno('Exit', 'Do you really want to exit?'):
        root.destroy()


title = Label(root, pady=5, text="Tussle Enterprises", bd=12, bg=bg_color, fg='black',
              font=('times new roman', 40, 'bold'), relief=GROOVE, justify=CENTER)
title.pack(fill=X)

# ===============Product Details=================
F1 = LabelFrame(root, text='Product Details', font=('times new roman', 26, 'bold',), fg='Purple', bg=bg_color, bd=15,
                relief=RIDGE)
F1.place(x=5, y=85, width=1000, height=715)

# ================== LOGO ===========================
'''
photo = Image.open("log.png", "r")
resize = photo.resize((151, 100))
img = ImageTk.PhotoImage(resize)

# x = LabelFrame(relief=RIDGE)
# x.place(x=6, y=90, width=810, height=605)
label1 = Label(image=img)
label1.image = resize
label1.place(x=0, y=0, height=0, width=0, relheight=1.0, relwidth=0, relx=100, rely=100)
label1.pack(padx=2, pady=2)
'''

# ===================== Heading ==========================
item = Label(F1, text='Items', font=('garamond', 20, 'bold', 'underline'), fg='black', bg=bg_color)
item.grid(row=0, column=0, padx=20, pady=15)

n = Label(F1, text='Quantity of Items', font=('garamond', 20, 'bold', 'underline'), fg='black', bg=bg_color)
n.grid(row=0, column=1, padx=30, pady=15)

cost = Label(F1, text='Cost of Items', font=('garamond', 20, 'bold', 'underline'), fg='black', bg=bg_color)
cost.grid(row=0, column=2, padx=30, pady=15)

# ===============Product============
two = Label(F1, text='Bailey [2L]', font=('garamond', 20, 'bold'), fg='green', bg=bg_color)
two.grid(row=1, column=0, padx=20, pady=15)
two_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=oneL, justify=CENTER)
two_txt.grid(row=1, column=1, padx=20, pady=15)
two_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=c_one, justify=CENTER)
two_txt.grid(row=1, column=2, padx=20, pady=15)

one = Label(F1, text='Bailey [1L]', font=('garamond', 20, 'bold'), fg='green', bg=bg_color)
one.grid(row=2, column=0, padx=20, pady=15)
one_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=twoL, justify=CENTER)
one_txt.grid(row=2, column=1, padx=20, pady=15)
one_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=c_two, justify=CENTER)
one_txt.grid(row=2, column=2, padx=20, pady=15)

half = Label(F1, text="Bailey [500ML]", font=('garamond', 20, 'bold'), fg='green', bg=bg_color)
half.grid(row=3, column=0, padx=20, pady=15)
half_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=halfL, justify=CENTER)
half_txt.grid(row=3, column=1, padx=20, pady=15)
half_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=c_half, justify=CENTER)
half_txt.grid(row=3, column=2, padx=20, pady=15)

quar = Label(F1, text="Bailey [250ML]", font=('garamond', 20, 'bold'), fg='green', bg=bg_color)
quar.grid(row=4, column=0, padx=20, pady=15)
quar_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=quaterL, justify=CENTER)
quar_txt.grid(row=4, column=1, padx=20, pady=15)
quar_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=c_quater, justify=CENTER)
quar_txt.grid(row=4, column=2, padx=20, pady=15)

t = Label(F1, text='Total', font=('garamond', 20, 'bold'), fg='green', bg=bg_color)
t.grid(row=5, column=0, padx=20, pady=15)
t_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=Total, justify=CENTER)
t_txt.grid(row=5, column=1, padx=20, pady=15)
totalcost_txt = Entry(F1, font='arial 15 bold', relief=SUNKEN, bd=7, textvariable=total_cost, justify=CENTER)
totalcost_txt.grid(row=5, column=2, padx=20, pady=15)

# ============================= Insert ==============================
Label(F1, text="Enter Client details ", font=("times new roman", 20, "bold", "underline"), bg=bg_color,
      fg="black", bd=0).grid(row=0, column=3, pady=15, padx=20)

company_name = Entry(F1, font=("helvetica", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=cname,
                     justify=CENTER)
company_name.insert(0, "Name/Company")
company_name.grid(row=1, column=3, padx=20, pady=15)

address = Entry(F1, font=("helvetica", 15, 'bold'), bg="white", relief=SUNKEN, bd=7, textvariable=add,
                justify=CENTER, )
address.insert(0, "Address")
address.grid(row=2, column=3, padx=20, pady=15)

state = Entry(F1, font=("helvetica", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=State,
              justify=CENTER)
state.insert(0, "State")
state.grid(row=3, column=3, padx=20, pady=15)

code = Entry(F1, font=("helvetica", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=pcode,
             justify=CENTER)
code.insert(0, "Postal-Code")
code.grid(row=4, column=3, padx=20, pady=15)

Email = Entry(F1, font=("helvetica", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=email,
              justify=CENTER)
Email.insert(0, "Email @gmail.com")
Email.grid(row=5, column=3, padx=20, pady=15)

cont = Entry(F1, font=("helvetica", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=contact,
             justify=CENTER)
cont.insert(0, "Contact Number")
cont.grid(row=6, column=3, padx=20, pady=15)

gate = Entry(F1, font=("helvetica", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=gateway,
             justify=CENTER)
gate.insert(0, "Offline")
gate.grid(row=9, column=0, padx=20, pady=15)

amt = Entry(F1, font=("impact", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=amount,
            justify=CENTER)
amt.insert(0, "Receive-Pay")
amt.grid(row=10, column=0, padx=20, pady=15)

inve = Entry(F1, font=("impact", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=invoice,
             justify=CENTER)
inve.insert(0, "Invoice Number")
inve.grid(row=10, column=1, padx=20, pady=15)

id = Entry(F1, font=("helvetica", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=tid,
           justify=CENTER)
id.insert(0, "Transaction-ID")
id.grid(row=9, column=1, padx=20, pady=15)

due = Entry(F1, font=("helvetica", 15, "bold"), bg="white", relief=SUNKEN, bd=7, textvariable=due_amount,
            justify=CENTER)
due.insert(0, "No-Dues")
due.grid(row=11, column=3, padx=20, pady=15)
# =====================Bill area====================
F2 = Frame(root, relief=GROOVE, bd=10)
F2.place(x=1000, y=80, width=430, height=500)

bill_title = Label(F2, text='Receipt', font='arial 15 bold', bd=7, relief=GROOVE).pack(fill=Y)
scrol_y = Scrollbar(F2, orient=VERTICAL)
scrol_y.pack(side=RIGHT, fill=Y)
textarea = Text(F2, font='arial 15', yscrollcommand=scrol_y.set)
textarea.pack(fill=BOTH)
scrol_y.config(command=textarea.yview)

# =====================Buttons========================
F3 = Frame(root, bg=bg_color, bd=15, relief=RIDGE)
F3.place(x=3, y=800, width=1070, height=95)

btn1 = Button(F3, text='Total', font='arial 25 bold', padx=5, pady=5, bg='white', fg='black', width=10, command=total)
btn1.grid(row=0, column=0, padx=20, pady=10)

btn2 = Button(F3, text='Receipt', font='arial 25 bold', padx=5, pady=5, bg='white', fg='black', width=10,
              command=receipt)
btn2.grid(row=0, column=1, padx=10, pady=10)

btn3 = Button(F3, text='Print', font='arial 25 bold', padx=5, pady=5, bg='white', fg='black', width=10,
              command=printout)
btn3.grid(row=0, column=2, padx=10, pady=10)

btn4 = Button(F3, text='Reset', font='arial 25 bold', padx=5, pady=5, bg='white', fg='black', width=10, command=reset)
btn4.grid(row=0, column=3, padx=10, pady=10)

btn5 = Button(F3, text='Exit', font='arial 25 bold', padx=5, pady=5, bg='white', fg='black', width=10, command=exit)
btn5.grid(row=0, column=4, padx=10, pady=10)

Radiobutton(F1, text='Paid', value=1, variable=selected, font=("impact", 25, "bold"), bg=bg_color, fg='maroon').grid(
    row=6, column=0)
Radiobutton(F1, text='Dues', value=2, variable=selected, font=("impact", 25, "bold"), bg=bg_color, fg='maroon').grid(
    row=6, column=1)
Radiobutton(F1, text='No Pay', value=3, variable=selected, font=("impact", 25, "bold"), bg=bg_color, fg='maroon').grid(
    row=6, column=2)

root.mainloop()
