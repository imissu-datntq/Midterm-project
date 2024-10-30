import csv
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
import tkinter as tk
from mydb import *
from tkinter import ttk
import datetime as dt
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Khởi tạo đối tượng database cho expense và income
expense_data = Database(db='finance.db', table_name='expense_record')

income_data = Database(db='finance.db', table_name='income_record')

# Biến toàn cục
count_ex = 0
selected_rowid_ex = 0
count_in = 0
selected_rowid_in = 0


def format_amount(amount):
        return f"{amount:,.0f}".replace(".", ",")
def parse_amount(amount_str):
    try:
        # Remove currency symbol and replace dots with nothing for conversion
        clean_str = amount_str.replace(",", "")
        return clean_str
    except ValueError:
        return 0.0

# Hàm lưu bản ghi expense
def saveRecord_ex():
    global count_ex
    # Lưu vào cơ sở dữ liệu
    expense_data.insert_ex(
        category_ex=category_var_ex.get(),
        name_ex=item_name_ex.get(),
        price_ex=int(item_amt_ex.get()),
        date_ex=transaction_date_ex.get()
    )
    # Hiển thị trên Treeview mà không gọi refresh ngay lập tức
    tv.insert(parent='', index = 0, iid=count_ex, values=(
        count_ex + 1,
        category_var_ex.get(),
        item_name_ex.get(),   
        format_amount(int(item_amt_ex.get())),
        transaction_date_ex.get()
    ))
    count_ex += 1

    clearEntries_ex()

# Thiết lập ngày hiện tại
def setDate_ex():
    date_ex = dt.datetime.now()
    dopvarex.set(f'{date_ex:%d %B %Y}')

# Xóa các trường nhập liệu
def clearEntries_ex():
    category_var_ex.set('')
    item_name_ex.delete(0, 'end')
    item_amt_ex.delete(0, 'end')
    transaction_date_ex.delete(0, 'end')

# Lấy các bản ghi từ database
def fetch_records_ex():
    global count_ex
    count_ex = len(expense_data.fetch_ex())
    records = expense_data.fetch_ex()
    for rec in records:
        if len(rec) == 5:
            tv.insert(parent='', index = 0, iid=count_ex, values=(rec[0], rec[1], rec[2], rec[3], rec[4]))
            count_ex += 1

# Chọn bản ghi để cập nhật
def select_record_ex(event):
    global selected_rowid_ex
    selected = tv.focus()    
    val = tv.item(selected, 'values')
    try:
        selected_rowid_ex = val[0]
        d = val[4]
        category_var_ex.set(val[1])
        namevarex.set(val[2])
        amtvarex.set(parse_amount(val[3]))
        dopvarex.set(str(d))
    except IndexError:
        pass

# Cập nhật bản ghi trong database
def update_record_ex():
    global selected_rowid_ex
    selected = tv.focus()
    try:
        # Cập nhật cơ sở dữ liệu
        expense_data.update_ex(
            rowid=selected_rowid_ex,
            category_ex=category_var_ex.get(),
            name_ex=namevarex.get(),
            price_ex=amtvarex.get(),
            date_ex=dopvarex.get()
        )
        
        # Cập nhật trên Treeview
        tv.item(selected, text="", values=(
            selected_rowid_ex,
            category_var_ex.get(),
            namevarex.get(),
            format_amount(amtvarex.get()),
            dopvarex.get()
        ))
    except Exception as ep:
        messagebox.showerror('Error', ep)

    clearEntries_ex()

# Tính tổng số dư giữa thu nhập và chi tiêu
def totalBalance():
    # Lấy tổng các bản ghi chi tiêu và thu nhập
    total_expense = expense_data.fetch_ex()
    total_income = income_data.fetch_in()
    
    # Tính tổng chi tiêu
    total_expense_sum = sum([(record[2]) for record in total_expense if record[2] not in [None, '']])
    # Tính tổng thu nhập
    total_income_sum = sum([(record[2]) for record in total_income if record[2] not in [None, '']])

    # Tính số dư còn lại
    balance_remaining = total_income_sum - total_expense_sum

    # Kiểm tra nếu số dư âm
    if balance_remaining < 0:
        messagebox.showwarning("Warning", f"You have overspent! 😡 TRY TO SPEND LESS!\nBalance Remaining: {format_amount(balance_remaining)} đ")
    else:
        messagebox.showinfo("Current Balance", f"Total Expense: {format_amount(total_expense_sum)}đ\nTotal Income: {format_amount(total_income_sum)}đ\nBalance Remaining: {format_amount(balance_remaining)}đ")

    
 

# Làm mới dữ liệu trong Treeview
def refreshData_ex():
    # Xóa tất cả bản ghi hiện có trong Treeview
    for item in tv.get_children():
        tv.delete(item)
    # Lấy lại tất cả các bản ghi từ database
    fetch_records_ex()

# Xóa bản ghi đã chọn
def deleteRow_ex():
    global selected_rowid_ex
    # Kiểm tra xem một hàng có được chọn không
    if selected_rowid_ex:
        # Xóa bản ghi trong database
        expense_data.remove_ex(selected_rowid_ex)
        
        # Xóa bản ghi trong Treeview
        selected = tv.selection()  # Lấy mục được chọn
        for item in selected:
            tv.delete(item)
        
        # Đặt lại `selected_rowid_ex`
        selected_rowid_ex = 0
    else:
        messagebox.showwarning("Warning", "Please select a record to delete.")
    clearEntries_ex()

def saveRecord_in():
    global count_in
    # Lưu vào cơ sở dữ liệu
    income_data.insert_in(
        category_in=category_var_in.get(),
        name_in=item_name_in.get(),
        price_in=int(item_amt_in.get()),
        date_in=transaction_date_in.get()
    )
    
    # Hiển thị trên Treeview mà không gọi refresh ngay lập tức
    zv.insert(parent='', index = 0, iid=count_in, values=(
        count_in + 1,
        category_var_in.get(),
        item_name_in.get(),
        format_amount(int(item_amt_in.get())),
        transaction_date_in.get()
    ))
    count_in += 1
    clearEntries_in()

# Thiết lập ngày hiện tại
def setDate_in():
    date_in = dt.datetime.now()
    dopvarin.set(f'{date_in:%d %B %Y}')

# Xóa các trường nhập liệu
def clearEntries_in():
    category_var_in.set('')
    item_name_in.delete(0, 'end')
    item_amt_in.delete(0, 'end')
    transaction_date_in.delete(0, 'end')

# Lấy các bản ghi từ database
def fetch_records_in():
    global count_in
    count_in = len(income_data.fetch_ex())
    records = income_data.fetch_in()
    for rec in records:
        if len(rec) == 5:
            zv.insert(parent='', index = 0, iid=count_in, values=(rec[0], rec[1], rec[2], rec[3], rec[4]))
            count_in += 1

# Chọn bản ghi để cập nhật
def select_record_in(event):
    global selected_rowid_in
    selected = zv.focus()    
    val = zv.item(selected, 'values')
    try:
        selected_rowid_in = val[0]
        d = val[4]
        category_var_in.set(val[1])
        namevarin.set(val[2])
        amtvarin.set(parse_amount(val[3]))
        dopvarin.set(str(d))
    except IndexError:
        pass

# Cập nhật bản ghi trong database
def update_record_in():
    global selected_rowid_in
    selected = zv.focus()
    try:
        # Cập nhật cơ sở dữ liệu
        income_data.update_in(
            rowid=selected_rowid_in,
            category_in=category_var_in.get(),
            name_in=namevarin.get(),
            price_in=amtvarin.get(),
            date_in=dopvarin.get()
        )
        
        # Cập nhật trên Treeview
        zv.item(selected, text="", values=(
            selected_rowid_in,
            category_var_in.get(),
            namevarin.get(),
            format_amount(amtvarin.get()),
            dopvarin.get()
        ))
    except Exception as ep:
        messagebox.showerror('Error', ep)

    clearEntries_in()

# Làm mới dữ liệu trong Treeview
def refreshData_in():
    # Xóa tất cả bản ghi hiện có trong Treeview
    for item in zv.get_children():
        zv.delete(item)
    # Lấy lại tất cả các bản ghi từ database
    fetch_records_in()

# Xóa bản ghi đã chọn
def deleteRow_in():
    global selected_rowid_in
    # Kiểm tra xem một hàng có được chọn không
    if selected_rowid_in:
        # Xóa bản ghi trong database
        income_data.remove_in(selected_rowid_in)
        
        # Xóa bản ghi trong Treeview
        selected = zv.selection()  # Lấy mục được chọn
        for item in selected:
            zv.delete(item)
        
        # Đặt lại `selected_rowid_ex`
        selected_rowid_in = 0
    else:
        messagebox.showwarning("Warning", "Please select a record to delete.")
    clearEntries_in()

def create_treeview(frame, columns, treeview_name):
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(expand=True, fill='both')
    return tree


ws = Tk()
ws.configure(bg="#abebea")
ws.title('Daily Expenses')
#ws.geometry("2000x2000")

f = ('Times new roman', 14)
category_var_ex = StringVar()
namevarex = StringVar()
amtvarex = IntVar()
dopvarex = StringVar()


category_var_in = StringVar()
namevarin = StringVar()
amtvarin = IntVar()
dopvarin = StringVar()

f2 = Frame(ws)
f2.pack() 

f1 = Frame(
    ws,
    padx=10,
    pady=10,
)
f1.pack(side = "left",expand=True, fill=BOTH) 
f4 = Frame(ws, padx=10, pady=10)
f4.pack(side="bottom", expand=True, fill=BOTH)

expense_label = Label(f2, text="Expense Records 💰                                    Income Records💸 ", font=("Arial", 12, "bold"))
expense_label.pack(side="top")

tv = ttk.Treeview(f2, columns=(1, 2, 3, 4,5), show='headings', height=8)
tv.pack(side = "left", expand=True, fill=BOTH)
##test 

 # Điều chỉnh vị trí tùy theo thiết kế của bạn

# Hàm tính và cập nhật total balance


Label(f1, text='EXPENSE_CATEGORY', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM NAME', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PRICE', font=f).grid(row=2, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=3, column=0, sticky=W)
# grid placement
categories_ex = ["Groceries", "Bills", "Entertainment", "Transport", "Others"]
category_var_ex.set("Select Category")
category_ex_menu = OptionMenu(f1, category_var_ex, *categories_ex)

#def show_selection():
 #   print(f"Selected category: {category_var.get()}")

category_ex_menu.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_name_ex = Entry(f1, font=f, textvariable=namevarex)
item_amt_ex = Entry(f1, font=f, textvariable=amtvarex)
transaction_date_ex = Entry(f1, font=f, textvariable=dopvarex)

# Entry grid placement

item_name_ex.grid(row=1, column=1, sticky=EW, padx=(10, 0))
item_amt_ex.grid(row=2, column=1, sticky=EW, padx=(10, 0))
transaction_date_ex.grid(row=3, column=1, sticky=EW, padx=(10, 0))
cur_date_ex = Button(
    f1, 
    text='Current Date', 
    font=f, 
    bg='#9da655', 
    command=setDate_ex,
    width=15
    )

submit_btn_ex = Button(
    f1, 
    text='Save Record', 
    font=f, 
    command=saveRecord_ex, 
    bg="#4ade3a", 
    fg='black'
    )

clr_btn_ex = Button(
    f1, 
    text='Clear Entry', 
    font=f, 
    command=clearEntries_ex, 
    bg='#4dad42', 
    fg='black'
    )

quit_btn_ex = Button(
    f1, 
    text='Exit', 
    font=f, 
    command=lambda:ws.destroy(), 
    bg='#71ad6a', 
    fg='black'
    )

total_bal_ex = Button(
    f1,
    text='Total Balance',
    font=("Times new roman",14),
    bg='#a65580',
    command=totalBalance,
    width=15,height = 3
)

total_spent_ex = Button(
    f1,
    text='Total Spent',
    font=f,
    command=lambda:expense_data.fetch_records_ex('select sum(ite)')
)

update_btn_ex = Button(
    f1, 
    text='Update',
    bg='#628f5d',
    command=update_record_ex,
    font=f
)

del_btn_ex = Button(
    f1, 
    text='Delete',
    bg='#3d6139',
    command=deleteRow_ex,
    font=f
)
cur_date_ex.grid(row=4, column=1, sticky=EW, padx=(10, 0))
submit_btn_ex.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn_ex.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn_ex.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal_ex.grid(row=5, column=3, sticky=EW, padx=(10, 0))
#total_bal_ex.place(relx=1, rely=0.5, anchor='center')
update_btn_ex.grid(row=3, column=2, sticky=EW, padx=(10, 0))
del_btn_ex.grid(row=4, column=2, sticky=EW, padx=(10, 0))


tv.column(1, anchor=CENTER, stretch=NO, width=30)
tv.column(2, anchor=CENTER,width=140)
tv.column(3, anchor=CENTER,width=150)
tv.column(4, anchor=CENTER,width=140)
tv.column(5, anchor=CENTER,width=140)
tv.heading(1, text="ID")
tv.heading(2, text="Category") 
tv.heading(3, text="Item Name", )
tv.heading(4, text="Item Price")
tv.heading(5, text="Purchase Date")

# INCOME 

zv = ttk.Treeview(f2, columns=(1, 2, 3, 4,5), show='headings', height=8)
zv.pack(side="right")

zv.column(1, anchor=CENTER, stretch=NO, width=30)
zv.column(2, anchor=CENTER,width=140)
zv.column(3, anchor=CENTER,width=150)
zv.column(4, anchor=CENTER,width=140)
zv.column(5, anchor=CENTER,width=140)
zv.heading(1, text="ID")
zv.heading(2, text="Category") 
zv.heading(3, text="Item Name", )
zv.heading(4, text="Item Price")
zv.heading(5, text="Purchase Date")
f3 = Frame(ws, padx=10, pady=10)
f3.pack(side="right", expand=True, fill=BOTH)
Label(f3, text='EXPENSE_CATEGORY', font=f).grid(row=0, column=0, sticky=W)
Label(f3, text='ITEM NAME', font=f).grid(row=1, column=0, sticky=W)
Label(f3, text='ITEM AMOUNT', font=f).grid(row=2, column=0, sticky=W)
Label(f3, text='INCOME DATE', font=f).grid(row=3, column=0, sticky=W)
#total_balance_label = Label(f3, font=("Arial", 20))
#total_balance_label.grid(row=6, column=0, sticky=W, padx=(10, 0)) 
balance_frame = Frame(f3, bd=2, relief="groove", padx=10, pady=10)
balance_frame.grid(row=6, column=0, sticky=W, padx=(10, 0), pady=10)

# Thêm nhãn `Total Balance` bên trong `balance_frame`
total_balance_label = Label(balance_frame, text="", font=("Times", 20,"italic"))
total_balance_label.pack()

def update_total_balance():
    # Tính toán balance từ các bản ghi
    total_expense_records = expense_data.fetch_ex()
    total_income_records = income_data.fetch_in()

    total_expense = sum([int(record[2]) for record in total_expense_records if record[2]])
    total_income = sum([int(record[2]) for record in total_income_records if record[2]])

    # Cập nhật giá trị balance
    balance = total_income - total_expense
    res = "{:,.0f}".format(balance).replace(".",",")
    total_balance_label.config(text=f"{res} đ ")
    #total_balance_label.config(text=f"{balance:.3f} đ ")

    # Gọi lại hàm này mỗi 1000ms (1 giây) để cập nhật
    ws.after(1000, update_total_balance)

# Gọi hàm cập nhật khi ứng dụng khởi chạy
update_total_balance()

categories_in = ["Salary", "Others"]
category_var_in.set("Select Category")
category_in_menu = OptionMenu(f3, category_var_in, *categories_in)
category_in_menu.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_name_in = Entry(f3, font=f, textvariable=namevarin)
item_amt_in = Entry(f3, font=f, textvariable=amtvarin)
transaction_date_in = Entry(f3, font=f, textvariable=dopvarin)

item_name_in.grid(row=1, column=1, sticky=EW, padx=(10, 0))
item_amt_in.grid(row=2, column=1, sticky=EW, padx=(10, 0))
transaction_date_in.grid(row=3, column=1, sticky=EW, padx=(10, 0))
cur_date_in = Button(
    f3, 
    text='Current Date', 
    font=f, 
    bg='#842ab8', 
    command=setDate_in,
    width=15
    )

submit_btn_in = Button(
    f3, 
    text='Save Record', 
    font=f, 
    command=saveRecord_in, 
    bg='#317cf5', 
    fg='black'
    )

clr_btn_in = Button(
    f3, 
    text='Clear Entry', 
    font=f, 
    command=clearEntries_in, 
    bg='#346ac2', 
    fg='black'
    )

quit_btn_in = Button(
    f3, 
    text='Exit', 
    font=f, 
    command=lambda:ws.destroy(), 
    bg='#345a99', 
    fg='black'
    )



total_spent_in = Button(
    f3,
    text='Total Spent',
    font=f,
    command=lambda:income_data.fetch_records_in('select sum(ite)')
)

update_btn_in = Button(
    f3, 
    text='Update',
    bg='#234987',
    command=update_record_in,
    font=f
)

del_btn_in = Button(
    f3, 
    text='Delete',
    bg='#1e3d6e',
    command=deleteRow_in,
    font=f
)
cur_date_in.grid(row=4, column=1, sticky=EW, padx=(10, 0))
submit_btn_in.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn_in.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn_in.grid(row=2, column=2, sticky=EW, padx=(10, 0))
update_btn_in.grid(row=3, column=2, sticky=EW, padx=(10, 0))
del_btn_in.grid(row=4, column=2, sticky=EW, padx=(10, 0))

for expense in expense_data.fetch_ex():
    tv.insert(parent='', index = 0, iid=count_ex, values=(
        count_ex + 1,
        expense[0],
        expense[1],   
        expense[2],
        expense[3]
    ))
    count_ex += 1
    
for income in income_data.fetch_ex():
    tv.insert(parent='', index = 0, iid=count_ex, values=(
        count_ex + 1,
        income[0],
        income[1],   
        income[2],
        income[3]
    ))
    count_ex += 1
    
# binding treeview
tv.bind("<ButtonRelease-1>", select_record_ex)
zv.bind("<ButtonRelease-1>", select_record_in)
#style for treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

#Vertical scrollbar
scrollbar1 = Scrollbar(f2, orient='vertical')
scrollbar1.configure(command=tv.yview)
scrollbar1.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar1.set)
scrollbar2 = Scrollbar(f2, orient='vertical')
scrollbar2.configure(command=zv.yview)
scrollbar2.pack(side="left", fill="y")
zv.config(yscrollcommand=scrollbar2.set)

# fetch_records_ex()
# fetch_records_in()

# infinite loop
ws.mainloop()