from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# Connect to MySQL database
try:
    con = mysql.connector.connect(host="localhost", user='root', password="Google@1", database="atm")
    cur = con.cursor()
     # Fetch data from 'customer' table
    cur.execute("select * from customer")
    rows = cur.fetchall()
    # Initialize lists to store customer data
    account_num = []
    cust_name = []
    balance = []
    pin = []
    # Populate lists with data from MySQL query
    for row in rows:
        account_num.append(row[0])
        cust_name.append(row[1])
        balance.append(row[2])
        pin.append(str(row[3]))

except Error as e:
    messagebox.showerror("Error", f"Error connecting to database: {e}")


# Hide all frames to show only the current frame
def hide_all_frames():
    for widget in root.winfo_children():
        widget.grid_forget()

# Login through pin

def pin_login():
    global pin_text
    hide_all_frames()
    pin_lable= Label(root, text="Enter PIN: ", font=("", 14, "bold"))
    pin_lable.grid(row=7, column=5, padx=10, pady=20)
    pin_text = Entry(root, font=("", 14),show="*")
    pin_text.grid(row=7, column=7, padx=10, pady=20)

    def validate_pin():
        global pin, cust_name
        if pin_text.get() in pin:
            index = pin.index(pin_text.get())
            messagebox.showinfo(f"Welcome ", f"Welcome {cust_name[index]}")
            show_main_menu()

        else:
            messagebox.showerror("Warning","Incorrect pin entred")
            pin_text.delete(0,'end')
    forget_pin_button = Button(root, text="Foget PIN", command=forget_pin, bg='#378620', fg='white', font=("", 10, 'bold'))
    forget_pin_button.grid(row=10, column=5, columnspan=2, padx=10, pady=20)
    login_button = Button(root, text="Login", command=validate_pin, bg='#378620', fg='white', font=("", 10, 'bold'))
    login_button.grid(row=10, column=7, columnspan=2, padx=10, pady=20)

# foget pin
def forget_pin():
    hide_all_frames()

    account_num_label = Label(root, text="Enter account number:", font=("", 14, "bold"))
    account_num_label.grid(row=8, column=5, padx=10, pady=20)
    account_num_entry = Entry(root, font=("", 14))
    account_num_entry.grid(row=8, column=7, padx=10, pady=20)

    new_pin_label = Label(root, text="Enter new PIN:", font=("", 14, "bold"))
    new_pin_label.grid(row=9, column=5, padx=10, pady=20)
    new_pin_entry = Entry(root, font=("", 14),show="*" ) 
    new_pin_entry.grid(row=9, column=7, padx=10, pady=20)

    confirm_pin_label = Label(root, text="Confirm new PIN:", font=("", 14, "bold"))
    confirm_pin_label.grid(row=10, column=5, padx=10, pady=20)
    confirm_pin_entry = Entry(root, font=("", 14),show="*") 
    confirm_pin_entry.grid(row=10, column=7, padx=10, pady=20)

     # validate Pin
    def check_new_pin():

        try:
                entered_account_num = int(account_num_entry.get())
        except ValueError:
                messagebox.showerror("Error", "Account number should be numeric")
                account_num_entry.delete(0, 'end')
                return

        if entered_account_num in account_num:
                if new_pin_entry.get() == confirm_pin_entry.get():
                    new_pin = new_pin_entry.get()
                    try:
                        cur.execute("UPDATE customer SET pin = %s WHERE account_num = %s", (new_pin, entered_account_num))
                        con.commit()
                        messagebox.showinfo("PIN Change", "PIN successfully changed")
                        pin_login()
                    except Error as e:
                        messagebox.showerror("Error", f"Error updating PIN: {e}")
                else:
                    messagebox.showerror("Error", "New PIN and Confirm PIN do not match")
                    new_pin_entry.delete(0, 'end')
                    confirm_pin_entry.delete(0, 'end')
        else:
                messagebox.showerror("Error", "Account number not found")
                account_num_entry.delete(0, 'end')
    back_button = Button(root, text="Back", command=pin_login, bg='#378620', fg='white', font=("", 10, 'bold'))
    back_button.grid(row=11, column=5, columnspan=2, padx=10, pady=20)
    
    change_button = Button(root, text="Change PIN", command=check_new_pin, bg='#378620', fg='white', font=("", 10, 'bold'))
    change_button.grid(row=11, column=7, columnspan=2, padx=10, pady=20)


# Display the balance inquiry frame
def balenq():
    hide_all_frames()
    global pin, balance,pin_text
    index = pin.index(pin_text.get())
    balance_label = Label(root, text=f"Your balance is: {balance[index]}", font=("", 14, "bold"))
    balance_label.grid(row=7, column=5, columnspan=2, padx=10, pady=20)
    back_button = Button(root, text="Back", command=show_main_menu, bg='#378620', fg='white', font=("", 10, 'bold'))
    back_button.grid(row=10, column=5, columnspan=2, padx=10, pady=20)

# Display the withdrawal frame 
def withdraw():
    hide_all_frames()
    withdraw_label = Label(root, text="Enter the amount: ", font=("", 14, "bold"))
    withdraw_label.grid(row=7, column=5, padx=10, pady=20)
    with_text = Entry(root, font=("", 14))
    with_text.grid(row=7, column=7, padx=10, pady=20)

    # Process the withdrawal
    def cash():
        global balance,pin
        try:
            cashw = float(with_text.get())
            index = pin.index(pin_text.get())
            
            if cashw > balance[index]:
                messagebox.showwarning("Insufficient Funds", "You do not have enough balance.")
            else:
                balance[index] -= cashw
                cur.execute("UPDATE customer SET balance = %s WHERE pin = %s",(balance[index],pin[index]))
                con.commit()
                messagebox.showinfo("Withdraw", f"{cashw} has been debited")
                show_main_menu()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    cw = Button(root, text="Withdraw", command=cash, bg='#378620', fg='white', font=("", 10, 'bold'))
    cw.grid(row=10, column=7, padx=10, pady=20)
    back_button = Button(root, text="Back", command=show_main_menu, bg='#378620', fg='white', font=("", 10, 'bold'))
    back_button.grid(row=10, column=5, padx=10, pady=20)


# Display the change PIN frame
def change_pin():
    hide_all_frames()
    current_pin_label = Label(root, text="Enter current PIN:", font=("", 14, "bold"))
    current_pin_label.grid(row=7, column=5, padx=10, pady=20)
    current_pin_entry = Entry(root, font=("", 14), show="*")
    current_pin_entry.grid(row=7, column=7, padx=10, pady=20)

    new_pin_label = Label(root, text="Enter new PIN:", font=("", 14, "bold"))
    new_pin_label.grid(row=8, column=5, padx=10, pady=20)
    new_pin_entry = Entry(root, font=("", 14), show="*")
    new_pin_entry.grid(row=8, column=7, padx=10, pady=20)

    confirm_pin_label = Label(root, text="Confirm new PIN:", font=("", 14, "bold"))
    confirm_pin_label.grid(row=9, column=5, padx=10, pady=20)
    confirm_pin_entry = Entry(root, font=("", 14), show="*")
    confirm_pin_entry.grid(row=9, column=7, padx=10, pady=20)

    # Process the PIN change
    def update_pin():
        global pin,account_num,pin_text
        index = pin.index(pin_text.get())
        if current_pin_entry.get() == pin_text.get():
            if new_pin_entry.get() == confirm_pin_entry.get():
                new_pin = new_pin_entry.get()
                try:
                    cur.execute("UPDATE customer SET pin = %s WHERE account_num = %s",(new_pin,account_num[index]))
                    con.commit()
                    messagebox.showinfo("PIN Change", "PIN successfully changed")
                    show_main_menu()
                except Error as e:
                    print(f"Error updating PIN: {e}")
            else:
                messagebox.showerror("Error", "New PIN and Confirm PIN do not match")
        else:
            messagebox.showerror("Error", "Current PIN is incorrect")

    change_button = Button(root, text="Change PIN", command=update_pin, bg='#378620', fg='white', font=("", 10, 'bold'))
    change_button.grid(row=10, column=7, padx=10, pady=20)
    back_button = Button(root, text="Back", command=show_main_menu, bg='#378620', fg='white', font=("", 10, 'bold'))
    back_button.grid(row=10, column=5, padx=10, pady=20)

# Display the main menu
def show_main_menu():
    hide_all_frames()
    be = Button(root, text="Balance Enquiry", command=balenq, bg='#378620', fg='white', font=("", 14, 'bold'))
    be.grid(row=3, column=0, padx=10, pady=20)

    cw = Button(root, text="Cash Withdrawal", command=withdraw, bg='#378620', fg='white', font=("", 14, 'bold'))
    cw.grid(row=3, column=1, padx=10, pady=20)

    cp = Button(root, text="Change PIN", command=change_pin, bg='#378620', fg='white', font=("", 14, 'bold'))
    cp.grid(row=4, column=0, padx=10, pady=20)

    lo = Button(root, text="log out", command=pin_login, bg='#378620', fg='white', font=("", 14, 'bold'))
    lo.grid(row=4, column=1, padx=10, pady=20)

# Initialize the main application window
root = Tk()
root.geometry("600x600")
root.title("ATM")

# Show login screen initially
pin_login()

# Start the main event loop
root.mainloop()
