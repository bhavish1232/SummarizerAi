from tkinter import *
from tkinter import ttk 
import ctypes
import time
import pyttsx3
import pygame
import os
import sys
import threading 
from datetime import datetime
from tkinter import filedialog, messagebox
import re 
import validators
import smtplib
from email.mime.text import MIMEText
from tkcalendar import DateEntry
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

BFrame = Frame(root, width=140, height=500, bg='#24344F', highlightbackground="white", highlightcolor="#1b2a41", highlightthickness=2).place(x=0, y=0)
CFrame = Frame(root, width=785, height=500, bg='#0f172a',highlightthickness=2).place(x=140, y=0)

heading = Label(root, text='Manage', fg='#FFFFFF', bg='#24344F', font=('Microsoft YaHei UI Light', 18, 'bold'))
heading.place(x=14, y=10)



#print("User ID -> ",end="")
#loguser = sys.argv[1]  
#adminPassword = sys.argv[2]
loguser = "aniketsingh123" 
adminPassword = "@niket123"
#print(loguser," ",adminPassword)

query.execute("select name,email from user where username=%s",(loguser,))
row = query.fetchone()
name = row[0]
email = row[1]


bgtrue = '#32CD32'
bgdef  = '#FF8C00'

def bgcolor(num):
    color_of_list = [User,Weblist,Music,Game]
    for i in range(len(color_of_list)):
        if (i + 1) == num:
            color_of_list[i].config(bg=bgtrue)
        else:
            color_of_list[i].config(bg=bgdef)


def user_manage():
   bgcolor(1)
   userFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)

   def check_user():
      username_text = userEntry.get().strip()
      if not username_text:
            messagebox.showwarning("Warning", "Please fill the Username field!")
            return
      
      query.execute("SELECT name,email,username,password FROM user WHERE username=%s",(username_text,))
      result = query.fetchone()
      if not result:
         messagebox.showerror("Not Found", "User not found!")
      else:
         new_window = Toplevel(root)  
         new_window.title("Update-Details")
         new_window.iconbitmap("logo.ico")
         new_window.geometry("670x380+450+225")
         new_window.configure(bg='#0f172a')
         new_window.resizable(False,False)
         

         def delete_profile():
            tables = ['user', 'blacklist', 'whitelist', 'focusrate', 'pomodoro']
            for table in tables:
              query.execute(f"DELETE FROM {table} WHERE username=%s", (username_text,))
              mydb.commit()

            messagebox.showinfo("Success!", "Profile Deleted Sucessfully!")
            new_window.destroy()
              


         def save_data():
            nameU = NameEntry.get().strip()
            emailU = EmailEntry.get().strip()
            usnU = usnEntry.get().strip()
            passU = passwoEntry.get().strip()
            

            if not nameU or not emailU or not usnU or not passU:
              messagebox.showerror("Error", "All fields are required!")
              return
            
            if not all(x.isalpha() or x.isspace() for x in nameU):
              messagebox.showerror("Error", "Name must contain only letters and spaces!")
              return

            if not re.match(r"[^@]+@[^@]+\.[^@]+", emailU):
              messagebox.showerror("Error", "Invalid Email Address!")
              return
            
            if not usnU.isalnum():
              messagebox.showerror("Error", "Username must be alphanumeric (only letters and numbers)!")
              return
            
            if not re.search(r'[A-Za-z]', usnU):
              messagebox.showerror("Error", "Username must contain at least one letter!")
              return
            
            if len(nameU) < 2 or len(usnU) < 3:
              messagebox.showerror("Error", "Name or Username too short!")
              return
            
            if len(passU) < 8:
              messagebox.showerror("Error", "Password must be at least 8 characters long!")
              return

            if not re.search(r'[A-Za-z]', passU):
              messagebox.showerror("Error", "Password must contain at least one letter (A-Z or a-z)!")
              return

            if not re.search(r'\d', passU):
              messagebox.showerror("Error", "Password must contain at least one number (0-9)!")
              return

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', passU):
              messagebox.showerror("Error", "Password must contain at least one special character (!@#$%^&* etc)!")
              return

            hashed_password = bcrypt.hashpw(passU.encode(), bcrypt.gensalt())
            query.execute("update user set name=%s, email=%s, password=%s where username=%s", (nameU, emailU, hashed_password,usnU))
            mydb.commit()
            messagebox.showinfo("Success!", "Data Saved Sucessfully!")
            new_window.destroy()


         Name = Label(new_window, text='  Name  ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 22, 'bold'))
         Name.place(x=50, y=20)
         NameEntry = Entry(new_window, width=25, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 22, 'bold'))
         NameEntry.place(x=220, y=20)
         NameEntry.insert(0,result[0])
         NameEntry.config(state="disabled")
        
         Email = Label(new_window, text='  Email  ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 22, 'bold'))
         Email.place(x=50, y=105)
         EmailEntry = Entry(new_window, width=25, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 22, 'bold'))
         EmailEntry.place(x=220, y=105)
         EmailEntry.insert(0,result[1])
         EmailEntry.config(state="disabled")

         usn = Label(new_window, text='Username  ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 22, 'bold'))
         usn.place(x=50, y=190)
         usnEntry = Entry(new_window, width=25, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 22, 'bold'))
         usnEntry.place(x=220, y=190)
         usnEntry.insert(0,result[2])
         usnEntry.config(state="disabled")
        

         passwo = Label(new_window, text='Password  ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 22, 'bold'))
         passwo.place(x=50, y=275)
         passwoEntry = Entry(new_window, width=25,show="*" ,fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 22, 'bold'))
         passwoEntry.place(x=220, y=275)
         passwoEntry.insert(0,result[3])
         passwoEntry.config(state="disabled")

         

         delete = Button(new_window, text="Delete", width=14, pady=5, bg='#DC143C', fg='#FFFFFF', 
                            font=("Microsoft YaHei UI Light", 10, "bold"),activebackground="#DC143C", activeforeground="#FFFFFF",command=delete_profile)
         delete.place(x=290, y=330)
        
     

   userLabel = Label(userFrame, text='Username : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 22, 'bold'))
   userLabel.place(x=190, y=20)
   userEntry = Entry(userFrame, width=25, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 22, 'bold'))
   userEntry.place(x=380, y=21)
   checkB = Button(userFrame, text="Check", width=6, pady=5, bg='#DC143C', fg='#FFFFFF', 
                            font=("Microsoft YaHei UI Light", 8, "bold"),activebackground="#DC143C", activeforeground="#FFFFFF",command=check_user)
   checkB.place(x=840, y=24)
   

def weblist():
    bgcolor(2)

    WhitelistFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)

    whitelist = []  
    whitelist_listbox = Listbox(WhitelistFrame, width=49, height=14, bg='white', fg='black', 
                                font=("Microsoft YaHei UI Light", 14), selectmode=SINGLE)
    whitelist_listbox.place(x=200, y=120)
    
    query.execute("SELECT title,weblink FROM weblist")
    rows = query.fetchall()
    
    for row in rows:
        tit = row[0]
        website = row[1]
        whitelist.append(website)
        whitelist_listbox.insert(END, tit+"  ->   "+website)  
        
    

        

    def add_url():
        url = url_entry.get().strip()
        title = url_Nentry.get().strip()
        if not title or title=="Enter Title here":
           messagebox.showerror("Error", "Please fill the Title.")
           return
        if len(title)>50:
             messagebox.showerror("Error", "Title too long! it shoudld be less than 50 character(including spaces)")
             return
        if not url:
           messagebox.showerror("Error","Please fill the URL")
           return
        
        if validators.url(url):
            if(url.endswith("/")):
                    url = url
            else:
                url = url + "/" 

            if (url not in whitelist) :
                current_date = datetime.now().strftime('%Y-%m-%d')  
            
                whitelist.append(url)
                whitelist_listbox.insert(END, title+"  ->   "+url)  
                url_entry.delete(0, END)
                url_Nentry.delete(0, END)  
            
            
                query.execute("INSERT INTO weblist(title,weblink,date) VALUES (%s, %s,%s)", (title,url, current_date))
                mydb.commit()
                messagebox.showinfo("Success", f"{url} has been added to the weblist.")
            
            else:
                messagebox.showwarning("Duplicate", f"{url} is already in the whitelist.")
        else:
            messagebox.showerror("Error", "Please enter a valid URL.")

    def remove_url():
        selected = whitelist_listbox.curselection()
        if selected:
            url = whitelist_listbox.get(selected)
            url = url.split('->')[1].strip()
            whitelist.remove(url)
            whitelist_listbox.delete(selected)
            query.execute(("delete from weblist where weblink=%s"),(url,))
            mydb.commit()
            messagebox.showinfo("Success", f"{url} has been removed from the weblist.")
        else:
            messagebox.showerror("Error", "Please select a URL to remove.")

    def remove_all():
        whitelist.clear()
        whitelist_listbox.delete(0, END)
        query.execute("delete from weblist")
        mydb.commit()
        messagebox.showinfo("Success", "All URLs have been removed from the weblist.")

    

    url_Nentry = Entry(WhitelistFrame, width=35, fg='black', border=2, bg="white", 
                      font=("Microsoft YaHei UI Light", 18, 'bold'))
    url_Nentry.place(x=225, y=13)
    url_Nentry.insert(0, "Enter Title here")
    def on_Nentry_click(event):
        if url_Nentry.get() == "Enter Title here":
            url_Nentry.delete(0, "end")

    def on_Nentry_focusout(event):
        if not url_Nentry.get():
            url_Nentry.insert(0, "Enter Title here")

    url_Nentry.bind("<FocusIn>", on_Nentry_click)
    url_Nentry.bind("<FocusOut>", on_Nentry_focusout)

    url_entry = Entry(WhitelistFrame, width=34, fg='black', border=2, bg="white", 
                      font=("Microsoft YaHei UI Light", 18, 'bold'))
    url_entry.place(x=226, y=62)
    url_entry.insert(0, "Enter URL here")

    def on_entry_click(event):
        if url_entry.get() == "Enter URL here":
            url_entry.delete(0, "end")

    def on_entry_focusout(event):
        if not url_entry.get():
            url_entry.insert(0, "Enter URL here")

    url_entry.bind("<FocusIn>", on_entry_click)
    url_entry.bind("<FocusOut>", on_entry_focusout)

    
    add_button = Button(WhitelistFrame, text="Add", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                        font=("Microsoft YaHei UI Light", 14, "bold"), 
                        command=add_url)
    add_button.place(x=769, y=200)

    
    
    remove_button = Button(WhitelistFrame, text="Remove", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                           font=("Microsoft YaHei UI Light", 14, "bold"), 
                           command=remove_url)
    remove_button.place(x=769, y=280)

    
    removebuttonall = Button(WhitelistFrame, text="Remove All", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                             font=("Microsoft YaHei UI Light", 14, "bold"), 
                             command=remove_all)
    removebuttonall.place(x=769, y=360)

   
    Idbutton = Button(WhitelistFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)


def music():
    bgcolor(3)

    WhitelistFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)

    whitelist = []  
    whitelist_listbox = Listbox(WhitelistFrame, width=49, height=14, bg='white', fg='black', 
                                font=("Microsoft YaHei UI Light", 14), selectmode=SINGLE)
    whitelist_listbox.place(x=200, y=120)

    def is_valid_music_file(file_path):
      music_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a']
      return os.path.exists(file_path) and any(file_path.lower().endswith(ext) for ext in music_extensions)
    
    query.execute("SELECT title,musiclink FROM musiclist")
    rows = query.fetchall()

    for row in rows:
        tit = row[0]
        website = row[1]
        whitelist.append(website)
        whitelist_listbox.insert(END, tit+"  ->   "+website)  
        
    

        

    def add_url():
        url = url_entry.get().strip()
        title = url_Nentry.get().strip()
        if not title or title=="Enter Music Title here":
           messagebox.showerror("Error", "Please fill the Music Title.")
           return
        if len(title)>50:
             messagebox.showerror("Error", "Title too long! it shoudld be less than 50 character(including spaces)")
             return
        if not url:
           messagebox.showerror("Error","Please provide the path of music")
           return
           
        if url:
            if url not in whitelist:
                current_date = datetime.now().strftime('%Y-%m-%d')  
            
                whitelist.append(url)
                whitelist_listbox.insert(END, title+"  ->   "+url)  
                url_entry.delete(0, END)
                url_Nentry.delete(0, END)  
            
            
                query.execute("INSERT INTO musiclist(title,musiclink,date) VALUES (%s, %s,%s)", (title,url, current_date))
                mydb.commit()
                messagebox.showinfo("Success", f"{url} has been added in the musiclist.")
            
            else:
                messagebox.showwarning("Duplicate", f"{url} is already in the Musiclist.")
        else:
            messagebox.showerror("Error", "Please enter a valid path.")

    def remove_url():
        selected = whitelist_listbox.curselection()
        if selected:
            url = whitelist_listbox.get(selected)
            url = url.split('->')[1].strip()
            whitelist.remove(url)
            whitelist_listbox.delete(selected)
            query.execute(("delete from musiclist where musiclink=%s"),(url,))
            mydb.commit()
            messagebox.showinfo("Success", f"{url} has been removed from the musiclist.")
        else:
            messagebox.showerror("Error", "Please select a path to remove.")

    def remove_all():
        whitelist.clear()
        whitelist_listbox.delete(0, END)
        query.execute("delete from musiclist")
        mydb.commit()
        messagebox.showinfo("Success", "All Music link have been removed from the musiclist.")

    

    url_Nentry = Entry(WhitelistFrame, width=35, fg='black', border=2, bg="white", 
                      font=("Microsoft YaHei UI Light", 18, 'bold'))
    url_Nentry.place(x=225, y=13)
    url_Nentry.insert(0, "Enter Music Title here")
    def on_Nentry_click(event):
        if url_Nentry.get() == "Enter Music Title here":
            url_Nentry.delete(0, "end")

    def on_Nentry_focusout(event):
        if not url_Nentry.get():
            url_Nentry.insert(0, "Enter Music Title here")

    url_Nentry.bind("<FocusIn>", on_Nentry_click)
    url_Nentry.bind("<FocusOut>", on_Nentry_focusout)

    url_entry = Entry(WhitelistFrame, width=34, fg='black', border=2, bg="white", 
                      font=("Microsoft YaHei UI Light", 18, 'bold'))
    url_entry.place(x=226, y=62)
    url_entry.insert(0, "Set Music link here")
    url_entry.config(state='disabled')

    def on_entry_click(event):
        if url_entry.get() == "Enter Music link here":
            url_entry.delete(0, "end")

    def on_entry_focusout(event):
        if not url_entry.get():
            url_entry.insert(0, "Enter Music link here")

    url_entry.bind("<FocusIn>", on_entry_click)
    url_entry.bind("<FocusOut>", on_entry_focusout)

    
    add_button = Button(WhitelistFrame, text="Add", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                        font=("Microsoft YaHei UI Light", 14, "bold"), 
                        command=add_url)
    add_button.place(x=769, y=200)

    
    
    remove_button = Button(WhitelistFrame, text="Remove", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                           font=("Microsoft YaHei UI Light", 14, "bold"), 
                           command=remove_url)
    remove_button.place(x=769, y=280)

    
    removebuttonall = Button(WhitelistFrame, text="Remove All", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                             font=("Microsoft YaHei UI Light", 14, "bold"), 
                             command=remove_all)
    removebuttonall.place(x=769, y=360)
    
    def browse_file():
        file = filedialog.askopenfilename()
        if is_valid_music_file(file):
            url_entry.config(state='normal')
            url_entry.delete(0, END)
            url_entry.insert(0, file)
            url_entry.config(state='disabled')
        else:
           messagebox.showerror("Invalid!", "Please enter a valid music file")

    browseButton = Button(WhitelistFrame, width=8, pady=7, text='Browse', borderwidth=3, bg='#DC143C', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#DC143C", activeforeground="#FFFFFF", command=browse_file)
    browseButton.place(x=730, y=62)

   
    Idbutton = Button(WhitelistFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)


def game():
    bgcolor(4)

    WhitelistFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)

    whitelist = []  
    whitelist_listbox = Listbox(WhitelistFrame, width=49, height=14, bg='white', fg='black', 
                                font=("Microsoft YaHei UI Light", 14), selectmode=SINGLE)
    whitelist_listbox.place(x=200, y=120)

    
    query.execute("SELECT title,gamelink FROM gamelist")
    rows = query.fetchall()

    for row in rows:
        tit = row[0]
        website = row[1]
        whitelist.append(website)
        whitelist_listbox.insert(END, tit+"  ->   "+website)  
        
    

        

    def add_url():
        url = url_entry.get().strip()
        title = url_Nentry.get().strip()
        if not title or title=="Enter Game Title here":
           messagebox.showerror("Error", "Please fill the Game Title.")
           return
        if len(title)>50:
             messagebox.showerror("Error", "Title too long! it shoudld be less than 50 character(including spaces)")
             return
        if not url:
           messagebox.showerror("Error","Please provide the path of Game")
           return
           
        if url:
            if url not in whitelist:
                current_date = datetime.now().strftime('%Y-%m-%d')  
            
                whitelist.append(url)
                whitelist_listbox.insert(END, title+"  ->   "+url)  
                url_entry.delete(0, END)
                url_Nentry.delete(0, END)  
            
            
                query.execute("INSERT INTO gamelist(title,gamelink,date) VALUES (%s, %s,%s)", (title,url, current_date))
                mydb.commit()
                messagebox.showinfo("Success", f"{url} has been added to the Gamelist.")
            
            else:
                messagebox.showwarning("Duplicate", f"{url} is already in the Gamelist.")
        else:
            messagebox.showerror("Error", "Please enter a valid path.")

    def remove_url():
        selected = whitelist_listbox.curselection()
        if selected:
            url = whitelist_listbox.get(selected)
            url = url.split('->')[1].strip()
            whitelist.remove(url)
            whitelist_listbox.delete(selected)
            query.execute(("delete from gamelist where gamelink=%s"),(url,))
            mydb.commit()
            messagebox.showinfo("Success", f"{url} has been removed from the Gamelist.")
        else:
            messagebox.showerror("Error", "Please select a path to remove.")

    def remove_all():
        whitelist.clear()
        whitelist_listbox.delete(0, END)
        query.execute("delete from gamelist")
        mydb.commit()
        messagebox.showinfo("Success", "All Games have been removed..")

    

    url_Nentry = Entry(WhitelistFrame, width=35, fg='black', border=2, bg="white", 
                      font=("Microsoft YaHei UI Light", 18, 'bold'))
    url_Nentry.place(x=225, y=13)
    url_Nentry.insert(0, "Enter Game Title here")
    def on_Nentry_click(event):
        if url_Nentry.get() == "Enter Game Title here":
            url_Nentry.delete(0, "end")

    def on_Nentry_focusout(event):
        if not url_Nentry.get():
            url_Nentry.insert(0, "Enter Game Title here")

    url_Nentry.bind("<FocusIn>", on_Nentry_click)
    url_Nentry.bind("<FocusOut>", on_Nentry_focusout)

    url_entry = Entry(WhitelistFrame, width=34, fg='black', border=2, bg="white", 
                      font=("Microsoft YaHei UI Light", 18, 'bold'))
    url_entry.place(x=226, y=62)
    url_entry.insert(0, "Enter Game link here")
    url_entry.config(state='disabled')

    def on_entry_click(event):
        if url_entry.get() == "Enter Game link here":
            url_entry.delete(0, "end")

    def on_entry_focusout(event):
        if not url_entry.get():
            url_entry.insert(0, "Enter Game link here")

    url_entry.bind("<FocusIn>", on_entry_click)
    url_entry.bind("<FocusOut>", on_entry_focusout)

    
    add_button = Button(WhitelistFrame, text="Add", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                        font=("Microsoft YaHei UI Light", 14, "bold"), 
                        command=add_url)
    add_button.place(x=769, y=200)

    
    
    remove_button = Button(WhitelistFrame, text="Remove", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                           font=("Microsoft YaHei UI Light", 14, "bold"), 
                           command=remove_url)
    remove_button.place(x=769, y=280)

    
    removebuttonall = Button(WhitelistFrame, text="Remove All", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                             font=("Microsoft YaHei UI Light", 14, "bold"), 
                             command=remove_all)
    removebuttonall.place(x=769, y=360)
    
   

    def browse_file():
        file = filedialog.askopenfilename()
        if file:
        
            disallowed_extensions = (
                '.mp3', '.wav', '.aac', '.flac',
                '.mp4', '.avi', '.mov', '.mkv',   
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'  
            )

        
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext in disallowed_extensions:
                messagebox.showerror("Invalid File", "Music, video, and image files are not allowed!")
            else:
                url_entry.config(state='normal')
                url_entry.delete(0, END)
                url_entry.insert(0, file)
                url_entry.config(state='disabled')
        else:
            messagebox.showerror("Invalid!", "Please enter a valid game file")


    browseButton = Button(WhitelistFrame, width=8, pady=7, text='Browse', borderwidth=3, bg='#DC143C', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#DC143C", activeforeground="#FFFFFF", command=browse_file)
    browseButton.place(x=730, y=62)

   
    Idbutton = Button(WhitelistFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)



    
User = Button(root, width=12, pady=7, text='User', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=user_manage)
User.place(x=17, y=62)
Weblist = Button(root, width=12, pady=7, text='Weblist', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=weblist)
Weblist.place(x=17, y=117)
Music = Button(root, width=12, pady=7, text='Music', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=music)
Music.place(x=17, y=170)
Game = Button(root, width=12, pady=7, text='Game', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=game)
Game.place(x=17, y=223)



def profile():
    ProfileFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)

    userprofile = Label(ProfileFrame, text="Admin-Profile", fg='#FF8C00', bg='#0f172a', font=('Microsoft YaHei UI Light', 28, 'bold'))
    userprofile.place(x=430, y=20)

    Name = Label(ProfileFrame, text='Name  :', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    Name.place(x=200, y=100)
    Nameans = Label(ProfileFrame, text=name, fg='#00CDEF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    Nameans.place(x=360, y=100)  
    
    Username = Label(ProfileFrame, text='Username  :', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    Username.place(x=200, y=280)
    Usernameans = Label(ProfileFrame, text=loguser, fg='#00CDEF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    Usernameans.place(x=410, y=280)  
    
    Email = Label(ProfileFrame, text='Email   :', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    Email.place(x=200, y=190)
    Emailans = Label(ProfileFrame, text=email, fg='#00CDEF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    Emailans.place(x=360, y=190)  
    
    User.config(bg='#FF8C00')
    Music.config(bg='#FF8C00')
    Game.config(bg='#FF8C00')

    def update_profile():
        new_window = Toplevel(root)  
        new_window.title("Update-Details")
        new_window.iconbitmap("logo.ico")
        new_window.geometry("670x380+450+225")
        new_window.configure(bg='#0f172a')
        new_window.resizable(False,False)

        
        def save_data():
            nameU = NameEntry.get().strip()
            emailU = EmailEntry.get().strip()
            usnU = usnEntry.get().strip()
            passU = passwoEntry.get().strip()
            

            if not nameU or not emailU or not usnU or not passU:
              messagebox.showerror("Error", "All fields are required!")
              return
            
            if not all(x.isalpha() or x.isspace() for x in nameU):
              messagebox.showerror("Error", "Name must contain only letters and spaces!")
              return

            if not re.match(r"[^@]+@[^@]+\.[^@]+", emailU):
              messagebox.showerror("Error", "Invalid Email Address!")
              return
            
            if not usnU.isalnum():
              messagebox.showerror("Error", "Username must be alphanumeric (only letters and numbers)!")
              return
            
            if not re.search(r'[A-Za-z]', usnU):
              messagebox.showerror("Error", "Username must contain at least one letter!")
              return
            
            if len(nameU) < 2 or len(usnU) < 3:
              messagebox.showerror("Error", "Name or Username too short!")
              return
            
            if len(passU) < 8:
              messagebox.showerror("Error", "Password must be at least 8 characters long!")
              return

            if not re.search(r'[A-Za-z]', passU):
              messagebox.showerror("Error", "Password must contain at least one letter (A-Z or a-z)!")
              return

            if not re.search(r'\d', passU):
              messagebox.showerror("Error", "Password must contain at least one number (0-9)!")
              return

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', passU):
              messagebox.showerror("Error", "Password must contain at least one special character (!@#$%^&* etc)!")
              return

            hashed_password = bcrypt.hashpw(passU.encode(), bcrypt.gensalt())
            query.execute("update admin set name=%s, email=%s, password=%s where username=%s", (nameU, emailU, hashed_password,usnU))
            mydb.commit()
            global name,email,adminPassword

            name = nameU
            email = emailU
            adminPassword = passU
            
            messagebox.showinfo("Success!", "Data Saved Sucessfully!")
            profile()
            new_window.destroy()


        Name = Label(new_window, text='  Name  ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 22, 'bold'))
        Name.place(x=50, y=20)
        NameEntry = Entry(new_window, width=25, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 22, 'bold'))
        NameEntry.place(x=220, y=20)
        NameEntry.insert(0,name)
        
        Email = Label(new_window, text='  Email  ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 22, 'bold'))
        Email.place(x=50, y=105)
        EmailEntry = Entry(new_window, width=25, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 22, 'bold'))
        EmailEntry.place(x=220, y=105)
        EmailEntry.insert(0,email)

        usn = Label(new_window, text='Username  ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 22, 'bold'))
        usn.place(x=50, y=190)
        usnEntry = Entry(new_window, width=25, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 22, 'bold'))
        usnEntry.place(x=220, y=190)
        usnEntry.insert(0,loguser)
        usnEntry.config(state="disabled")
        
        def seePass():
            if passwoEntry.cget('show') == '*':
                passwoEntry.config(show='')  
            else:
                passwoEntry.config(show='*')

        passwo = Label(new_window, text='Password  ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 22, 'bold'))
        passwo.place(x=50, y=275)
        passwoEntry = Entry(new_window, width=22,show="*" ,fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 22, 'bold'))
        passwoEntry.place(x=220, y=275)
        passwoEntry.insert(0,adminPassword)
        onbutton = Button(new_window, width=6, pady=7, text='👁️', borderwidth=3, bg='#0f172a', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 8, "bold"), activebackground="#0f172a", activeforeground="#FFFFFF",command=seePass)
        onbutton.place(x=615, y=275)

        save = Button(new_window, text="Save", width=10, pady=5, bg='#32CD32', fg='#FFFFFF', 
                            font=("Microsoft YaHei UI Light", 10, "bold"),command=save_data)
        save.place(x=350, y=330)
        
        



        

    password = Label(ProfileFrame, text='Password   :', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    password.place(x=200, y=370)
    passwordans = Label(ProfileFrame, text="*************", fg='#00CDEF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    passwordans.place(x=430, y=378)  
    

    update = Button(ProfileFrame, text="Update-Details", width=14, pady=5, bg='#DC143C', fg='#FFFFFF', 
                            font=("Microsoft YaHei UI Light", 10, "bold"),activebackground="#DC143C", activeforeground="#FFFFFF",command=update_profile)
    update.place(x=480, y=442)

profile()


root.mainloop()

