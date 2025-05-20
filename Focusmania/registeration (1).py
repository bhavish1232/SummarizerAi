from tkinter import *
from tkinter import messagebox
import subprocess
import re
import mysql.connector as MyConn
import bcrypt


mydb = MyConn.connect(host="localhost", user="root", password="Aa@9724601978!", database="focusmania")
query = mydb.cursor()



def open_login():
    window.destroy()
    subprocess.run(["python", "Login.py"]) 

def sign_up():
    name_value = name.get().strip()  
    username_value = user.get().strip().lower()  
    email_value = code.get().strip().lower()  
    password_value = confirm_code.get().strip()  

    if not name_value or not username_value or not email_value or not password_value:
        messagebox.showerror("Missing", "Please fill out all the information.")
        return
    if not all(x.isalpha() or x.isspace() for x in name_value):
              messagebox.showerror("Error", "Name must contain only letters and spaces!")
              return
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email_value):
              messagebox.showerror("Error", "Invalid Email Address!")
              return
    if not username_value.isalnum():
              messagebox.showerror("Error", "Username must be alphanumeric (only letters and numbers)!")
              return
    if not re.search(r'[A-Za-z]', username_value):
              messagebox.showerror("Error", "Username must contain at least one letter!")
              return
            
    if len(name_value) < 2 or len(username_value) < 3:
              messagebox.showerror("Error", "Name or Username too short!")
              return
            
    if len(password_value) < 8:
              messagebox.showerror("Error", "Password must be at least 8 characters long!")
              return

    if not re.search(r'[A-Za-z]', password_value):
              messagebox.showerror("Error", "Password must contain at least one letter (A-Z or a-z)!")
              return

    if not re.search(r'\d', password_value):
              messagebox.showerror("Error", "Password must contain at least one number (0-9)!")
              return

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password_value):
              messagebox.showerror("Error", "Password must contain at least one special character (!@#$%^&* etc)!")
              return
    
    else:
        query.execute("SELECT * FROM user WHERE username=%s OR email=%s", (username_value, email_value))
        existing_user = query.fetchone()

        if existing_user:
            messagebox.showerror("Signup Failed!", "Username or Email already exists. Try another one!")
        else:
            
            hashed_password = bcrypt.hashpw(password_value.encode(), bcrypt.gensalt())

            
            query.execute("INSERT INTO user(name, username, email, password) VALUES (%s, %s, %s, %s)",
                          (name_value, username_value, email_value, hashed_password))
            mydb.commit()
            messagebox.showinfo("Done", "You have signed up successfully!")

window = Tk()
window.title("Focusmania")
window.iconbitmap("logo.ico")
window.geometry('925x500+250+120')
window.configure(bg='#0f172a') 
window.resizable(False, False)

img = PhotoImage(file='login.png')
Label(window, image=img, borderwidth=3, bg="#f0f4f8").place(x=50, y=65)

frame = Frame(window, width=350, height=430, bg='#1b2a41')
frame.place(x=500, y=30)

heading = Label(frame, text='Sign up', fg='#FF8C00', bg='#1b2a41', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=110, y=5)

def on_enter(e):
    name.delete(0, 'end')

def on_leave(e):
    nam = name.get()
    if nam == "":
        name.insert(0, 'Name')

name = Entry(frame, width=25, fg='#FFFFFF', border=0, bg="#1b2a41", font=("Microsoft YaHei UI Light", 11, 'bold'))
name.place(x=30, y=80)
name.insert(0, 'Name')
name.bind('<FocusIn>', on_enter)
name.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='#FF8C00').place(x=28, y=105)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    nam = user.get()
    if nam == "":
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='#FFFFFF', border=0, bg="#1b2a41", font=("Microsoft YaHei UI Light", 11,'bold'))
user.place(x=30, y=150)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='#FF8C00').place(x=28, y=175)

def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    email = code.get()
    if email == "":
        code.insert(0, 'Email')

code = Entry(frame, width=25, fg='#FFFFFF', border=0, bg="#1b2a41", font=("Microsoft YaHei UI Light", 11, 'bold'))
code.place(x=30, y=220)
code.insert(0, 'Email')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='#FF8C00').place(x=28, y=245)

def on_enter(e):
    confirm_code.delete(0, 'end')

def on_leave(e):
    confirm_password = confirm_code.get()
    if confirm_password == "":
        confirm_code.insert(0, 'Confirm Password')

confirm_code = Entry(frame, width=25, fg='#FFFFFF', border=0, bg="#1b2a41", font=("Microsoft YaHei UI Light", 11,'bold'))
confirm_code.place(x=30, y=290)
confirm_code.insert(0, 'Set Password')
confirm_code.bind('<FocusIn>', on_enter)
confirm_code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='#FF8C00').place(x=28, y=315)

Button(frame, width=20, pady=7, text='Sign up', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=sign_up).place(x=95, y=350) 
label = Label(frame, text='Already have an account?', fg='#FFFFFF', bg='#1b2a41', font=('Microsoft YaHei UI Light', 8, 'bold')) 
label.place(x=77, y=400)

signin = Button(frame, width=6, text='Sign in', border=0, bg='#1b2a41', cursor='hand2', fg='#FF8C00', activebackground='#1b2a41', activeforeground='#FF8C00', command=open_login)
signin.place(x=234, y=400)

window.mainloop()
