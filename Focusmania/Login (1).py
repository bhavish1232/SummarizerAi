from tkinter import *
from tkinter import messagebox
import subprocess  
import mysql.connector as MyConn
import bcrypt


mydb = MyConn.connect(host="localhost", user="root", password="Aa@9724601978!", database="focusmania")
query = mydb.cursor()

root = Tk()
root.title("Focusmania")
root.iconbitmap("logo.ico")
root.geometry("925x500+250+120")
root.configure(bg='#0f172a')
root.resizable(False, False)

def sign_in():
    username = user.get().strip().lower()  
    password = code.get().strip()

    if not username or not password:
        messagebox.showerror("Missing", "Please enter both username and password.")
        return

    
    query.execute("SELECT password FROM user WHERE username=%s", (username,))
    result = query.fetchone()

    if result is None:
        messagebox.showerror("Login Failed", "Your username is incorrect. Try again!")
    else:
        stored_hashed_password = result[0]  

        
        if bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
            root.destroy()
            subprocess.run(["python", "focusmania.py",username,password],shell=True)
        else:
            messagebox.showerror("Login Failed", "Your password is incorrect. Try again!")
    
    

def open_registration():
    root.destroy() 
    subprocess.Popen(['python', 'registeration.py']) 

img = PhotoImage(file='login.png')
Label(root, image=img, borderwidth=3, bg="#f0f4f8").place(x=50, y=65)

frame = Frame(root, width=350, height=350, bg="#1b2a41")
frame.place(x=500, y=60)

heading = Label(frame, text='Sign in', fg='#FF8C00', bg='#1b2a41', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=110, y=5)

def on_enter_user(e):
    user.delete(0, 'end')

def on_leave_user(e):
    name = user.get()
    if name == "":
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='#FFFFFF', border=0, bg="#1b2a41", font=("Microsoft YaHei UI Light", 11, 'bold'))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter_user)
user.bind('<FocusOut>', on_leave_user)

Frame(frame, width=295, height=2, bg='#FF8C00').place(x=28, y=105)

def on_enter_code(e):
    code.delete(0, 'end')

def on_leave_code(e):
    password = code.get()
    if password == "":
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='#FFFFFF', border=0, bg="#1b2a41" ,font=("Microsoft YaHei UI Light", 11, 'bold'))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter_code)
code.bind('<FocusOut>', on_leave_code)

Frame(frame, width=295, height=2, bg='#FF8C00').place(x=28, y=175)

Button(frame, width=20, pady=7, text='Sign in', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0,
       font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",
       command=sign_in).place(x=90, y=228)
label = Label(frame, text="Don't have an account?", fg='#FFFFFF', bg='#1b2a41', font=("Helvetica", 9, "bold"))
label.place(x=85, y=280)
sign_up = Button(frame, width=6, text='Sign up', border=0, bg='#1b2a41', cursor='hand2', fg='#FF8C00',
                 activebackground="#1b2a41", activeforeground="#FF8C00", command=open_registration)
sign_up.place(x=225, y=280)

root.mainloop()
