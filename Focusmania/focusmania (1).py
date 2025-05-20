from tkinter import *
from tkinter import ttk 
import ctypes
import time
import pyttsx3
import pygame
import subprocess  
import os
import sys
import validators
import threading 
from datetime import datetime,date
from tkinter import filedialog, messagebox
import re 
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

heading = Label(root, text='Features', fg='#FFFFFF', bg='#24344F', font=('Microsoft YaHei UI Light', 18, 'bold'))
heading.place(x=14, y=10)



print("User ID -> ",end="")
#loguser = sys.argv[1]  
#userPassword = sys.argv[2]
loguser = "aniketsingh123"
#print(loguser)
userPassword = "123456"
#print (userPassword)

query.execute("select name,email from user where username=%s",(loguser,))
row = query.fetchone()
name = row[0]
email = row[1]


bgtrue = '#32CD32'
bgdef  = '#FF8C00'

def bgcolor(num):
    color_of_list = [Blacklist, Whitelist, FocusButton, Pomodoro, Reminder, Music, Game, Analysis]
    for i in range(len(color_of_list)):
        if (i + 1) == num:
            color_of_list[i].config(bg=bgtrue)
        else:
            color_of_list[i].config(bg=bgdef)


def blockweb():
    bgcolor(1)
    BlockFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)

    
    

    url = Label(BlockFrame, text='URL :', fg='#FFFFFF', bg='#24344F', font=('Microsoft YaHei UI Light', 40, 'bold'))
    url.place(x=220, y=80)

    code = Entry(BlockFrame, width=16, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 40, 'bold'))
    code.place(x=390, y=80)
    code.insert(0, 'https://www.facebook.com/')
    
    new_window = None

    def check_list():
        nonlocal new_window

        if new_window is not None and new_window.winfo_exists():
            new_window.destroy()

        new_window = Toplevel(root)  
        new_window.title("Popular Websites")
        new_window.iconbitmap("logo.ico")
        new_window.geometry("350x250+570+330")
        new_window.resizable(False,False)
        v_scrollbar = Scrollbar(new_window, orient=VERTICAL)
        h_scrollbar = Scrollbar(new_window, orient=HORIZONTAL)
        weblist = Listbox(new_window, width=23, height=8, bg='#24344F', fg='#FFFFFF', 
                                font=("Microsoft YaHei UI Light", 20, 'bold'), selectmode=SINGLE,yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        weblist.place(x=0, y=0)
        v_scrollbar.config(command=weblist.yview)
        h_scrollbar.config(command=weblist.xview)

        v_scrollbar.place(x=23, y=0, height=220)  
        h_scrollbar.place(x=0, y=8, width=330) 
        query.execute("SELECT title,weblink FROM weblist")
        rows = query.fetchall()
        popularWebsiteList = []
        websiteItems = []

        for title,weblink in rows:
            websiteItems.append(title)
            popularWebsiteList.append(weblink)

        for item in websiteItems:
                weblist.insert(END, item)

        def show_index(event):
            selected_index = weblist.curselection()
            if selected_index:  
                code.delete(0, END)
                code.insert(0, popularWebsiteList[selected_index[0]])
            else:
                 print("did not selected")
        
        weblist.bind("<<ListboxSelect>>", show_index)


    def block_website_action():
        url = code.get().strip()
        if not url:
            url = "https://www.facebook.com/"

        query.execute("select website from blacklist where username=%s",(loguser,))
        checkifBlock=query.fetchall()
        newCheckBlock = []
        for i in checkifBlock:
            newCheckBlock.append(i[0])
        


        

        if validators.url(url):

            url = re.sub(r'^http[s]?://', '', url)  
            url = url.split('/')[0]  

            if url in newCheckBlock:
                messagebox.showinfo(f"Blocked Already", f"This {url} has been blocked already!")
                return

            hosts_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"  

            try:
                with open(hosts_file, "a") as file:
                
                    file.write(f"\n127.0.0.1 {url}\n")
                    file.write(f"127.0.0.1 www.{url}\n")  
                    current_date = datetime.now().strftime('%Y-%m-%d') 
                    query.execute("INSERT INTO blacklist(username, website, date) VALUES (%s, %s, %s)", (loguser, url, current_date))
                    mydb.commit()
                    messagebox.showinfo("Success", f"The website {url} has been blocked successfully.")
            except PermissionError:
                messagebox.showerror("Permission Denied", "You need administrator permissions to block a website. Please run the program as Administrator.")
            except Exception as e:
                messagebox.showerror("Error", f"You have already blocked {url}")

        else:
           messagebox.showerror("Error", f"Invalid URL : {url}") 

    def unblock_website_action():
        url = code.get().strip()
        if not url:
            url = "https://www.facebook.com/"

        query.execute("select website from blacklist where username=%s",(loguser,))
        checkifBlock=query.fetchall()
        newCheckBlock = []
        for i in checkifBlock:
            newCheckBlock.append(i[0])
    
        
        

        if validators.url(url):
            url = re.sub(r'^http[s]?://', '', url) 
            url = url.split('/')[0]  
            
            if url not in newCheckBlock:
                messagebox.showinfo(f"Haven't Blocked Yet!", f"This {url} has not been blocked")
                return

            hosts_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"  

            try:
                with open(hosts_file, "r") as file:
                    lines = file.readlines()

                with open(hosts_file, "w") as file:
                    for line in lines:
                        if url not in line and f"www.{url}" not in line:
                            file.write(line)
                query.execute(("delete from blacklist where website=%s"),(url,))
                mydb.commit()
                messagebox.showinfo("Success", f"The website {url} has been unblocked successfully.")
            except PermissionError:
                messagebox.showerror("Permission Denied", "You need administrator permissions to unblock a website. Please run the program as Administrator.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while unblocking the website: {e}")
        else:
            messagebox.showinfo("Failed", f"Invalid URL : {url}")
    BlockWebsite = Button(BlockFrame, width=20, pady=7, text='Block', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 20, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=block_website_action).place(x=330, y=230)
    UnblockWebsite = Button(BlockFrame, width=20, pady=7, text='Unblock', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 20, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=unblock_website_action).place(x=330, y=330)
    listButton = Button(BlockFrame, width=20, pady=7, text='see popular websites', borderwidth=3, bg='#0f172a', fg='#FF8C00', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 12, "bold"),activebackground="#0f172a", activeforeground="#FF8C00", command=check_list)
    listButton.place(x=700, y=450)
    Idbutton = Button(BlockFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)


def whitelistweb():
    bgcolor(2)

    WhitelistFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)

    whitelist = []  
    whitelist_listbox = Listbox(WhitelistFrame, width=49, height=14, bg='white', fg='black', 
                                font=("Microsoft YaHei UI Light", 14), selectmode=SINGLE)
    whitelist_listbox.place(x=200, y=120)
    
    query.execute("SELECT website FROM whitelist WHERE username = %s", (loguser,))
    rows = query.fetchall()

    for row in rows:
        website = row[0]
        whitelist.append(website)
        whitelist_listbox.insert(END, website)  
        
    

   
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    redirect_ip = "127.0.0.1"

        
        

    def add_url():
        url = url_entry.get().strip()
        if validators.url(url):
            if(url.endswith("/")):
                    url = url
            else:
                url = url + "/"
            if (url not in whitelist):
                current_date = datetime.now().strftime('%Y-%m-%d')  
            
                whitelist.append(url)

                
                                
                whitelist_listbox.insert(END, url)  
                url_entry.delete(0, END)  
            
            
                query.execute("INSERT INTO whitelist(username, website, date) VALUES (%s, %s, %s)", (loguser, url, current_date))
                mydb.commit()
            
                messagebox.showinfo("Success", f"{url} has been added to the whitelist.")
            else:
                messagebox.showwarning("Duplicate", f"{url} is already in the whitelist.")
        else:
            messagebox.showerror("Error", "Please enter a valid URL.")

    def remove_url():
        selected = whitelist_listbox.curselection()
        if selected:
            url = whitelist_listbox.get(selected)
            whitelist.remove(url)
            whitelist_listbox.delete(selected)
            query.execute(("delete from whitelist where website=%s"),(url,))
            mydb.commit()
            messagebox.showinfo("Success", f"{url} has been removed from the whitelist.")
        else:
            messagebox.showerror("Error", "Please select a URL to remove.")

    def remove_all():
        whitelist.clear()
        whitelist_listbox.delete(0, END)
        query.execute(("delete from whitelist where username=%s"),(loguser,))
        mydb.commit()
        messagebox.showinfo("Success", "All URLs have been removed from the whitelist.")

    def apply_whitelist():
        
        permissionDeniedTracker = False

        def block_website(url):

            nonlocal permissionDeniedTracker
           
            url = re.sub(r'^http[s]?://', '', url) 
            url = url.split('/')[0] 

            hosts_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"  
            try:
                with open(hosts_file, "a") as file:
                    
                    file.write(f"\n127.0.0.1 {url}\n")
                    file.write(f"127.0.0.1 www.{url}\n")  
            except PermissionError:
                messagebox.showerror("Permission Denied", "You need administrator permissions to block a website. Please run the program as Administrator.")
                permissionDeniedTracker = True
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while blocking the website: {e}")

        def unblock_website(urllink):

            
            urllink = re.sub(r'^http[s]?://', '', urllink)  
            urllink = urllink.split('/')[0]  

            
            hosts_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"  

        
            with open(hosts_file, "r") as file:
                lines = file.readlines()

            with open(hosts_file, "w") as file:
                for line in lines:
                    if urllink not in line and f"www.{urllink}" not in line:
                        file.write(line)
        
        Blocklist = [
                'https://www.instagram.com/', 'https://twitter.com/', 'https://x.com/',
                'https://www.facebook.com/', 'https://www.snapchat.com/', 'https://www.tiktok.com/',
                'https://www.reddit.com/', 'https://www.youtube.com/', 'https://www.netflix.com/',
                'https://www.disneyplus.com/', 'https://www.primevideo.com/', 'https://www.hulu.com/',
                'https://www.twitch.tv/', 'https://www.roblox.com/', 'https://steamcommunity.com/',
                'https://www.epicgames.com/', 'https://www.miniclip.com/', 'https://www.addictinggames.com/',
                'https://www.amazon.com/', 'https://www.ebay.com/', 'https://www.flipkart.com/',
                'https://www.aliexpress.com/', 'https://www.buzzfeed.com/', 'https://www.tmz.com/',
                'https://www.9gag.com/', 'https://www.boredpanda.com/', 'https://web.whatsapp.com/',
                'https://www.discord.com/', 'https://web.telegram.org/', 'https://web.snapchat.com/'
                    ]
        
        for url in Blocklist:
            if (permissionDeniedTracker == False) :
                block_website(url)
            else:
                break
               


        listbox = list(whitelist_listbox.get(0, END))
        for urllink in listbox:
            unblock_website(urllink)

        messagebox.showinfo("Sucess","Only Listbox website would be accesible now!")
            


            
    def disable_whitelist():

        def unblock_website(urllink):

            
            urllink = re.sub(r'^http[s]?://', '', urllink)  
            urllink = urllink.split('/')[0]  

           
            hosts_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"  

        
            with open(hosts_file, "r") as file:
                lines = file.readlines()

            with open(hosts_file, "w") as file:
                for line in lines:
                    if urllink not in line and f"www.{urllink}" not in line:
                        file.write(line)
        
        Blocklist = ['https://www.instagram.com/','https://twitter.com/', 'https://x.com/',
                     'https://www.facebook.com/',  'https://www.snapchat.com/'
                    ]

        for urllink in Blocklist:
            unblock_website(urllink)

        messagebox.showinfo("Sucess","All website would be accesible now!")
            
        


   
    url_entry = Entry(WhitelistFrame, width=39, fg='black', border=2, bg="white", 
                      font=("Microsoft YaHei UI Light", 18, 'bold'))
    url_entry.place(x=195, y=60)
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
    add_button.place(x=769, y=150)

    
    
    remove_button = Button(WhitelistFrame, text="Remove", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                           font=("Microsoft YaHei UI Light", 14, "bold"), 
                           command=remove_url)
    remove_button.place(x=769, y=220)

    
    removebuttonall = Button(WhitelistFrame, text="Remove All", width=10, pady=5, bg='#FF8C00', fg='#FFFFFF', 
                             font=("Microsoft YaHei UI Light", 14, "bold"), 
                             command=remove_all)
    removebuttonall.place(x=769, y=290)

   
    apply_button = Button(WhitelistFrame, text="ON", width=10, pady=5, bg='#32CD32', fg='#FFFFFF', 
                          font=("Microsoft YaHei UI Light", 14, "bold"), 
                          command=apply_whitelist)
    apply_button.place(x=769, y=360)

    
    disable_button = Button(WhitelistFrame, text="OFF", width=10, pady=5, bg='#DC143C', fg='#FFFFFF', 
                            font=("Microsoft YaHei UI Light", 14, "bold"), 
                            command=disable_whitelist)
    disable_button.place(x=769, y=430)
    Idbutton = Button(WhitelistFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)


def focusmode():
    bgcolor(3)

    global session_ended_manually
    session_ended_manually = False
    haveYouOn = False


  
    def hide_taskbar():
        ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None), 0)

   
    def show_taskbar():
        ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None), 1)

    
    def hide_desktop_icons():
        ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Progman", None), 0)

    
    def show_desktop_icons():
        ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Progman", None), 5)

    
    def launch_focus_activity():
        file = appname.get()
        if file:
            try:
                os.startfile(file)
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found! Please select a valid file.")

   
    def focus_on():
        global session_ended_manually  
        
        nonlocal haveYouOn
        
        
        pathdata=appname.get().strip()
        if not pathdata:
            messagebox.showerror("Error","Please select a file")
            return
        timedata = timerset.get().strip()
        if not timedata:
            messagebox.showerror("Error","Timeinput can't be blank")
            return
        if "." in timedata:
            messagebox.showerror("Error","Timeinput can't be Fraction")
            return
        

        if timedata.isdigit():
            timedata = int(timedata)
            if(timedata==0):
                 messagebox.showerror("Error","Timeinput can't be zero")
                 return
            
            try:
                session_ended_manually = False  
                haveYouOn = True
                hide_taskbar()
                hide_desktop_icons()
                launch_focus_activity()

                focus_time = int(timerset.get()) * 60  
                threading.Thread(target=focus_timer, args=(focus_time,), daemon=True).start()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid time in minutes.")
        
        else:
           messagebox.showerror("Error", "Please enter a valid time in minutes.") 
           return
        

        

    
    def focus_timer(focus_time):
        global session_ended_manually 

        while focus_time > 0:
           
            if session_ended_manually:
                break

            minutes, seconds = divmod(focus_time, 60)
            timer_label.config(text=f"Time Left: {minutes:02d}:{seconds:02d}")
            time.sleep(1)  
            focus_time -= 1

        
        if not session_ended_manually:
            show_taskbar()  
            show_desktop_icons()  
            current_date = datetime.now().strftime('%Y-%m-%d')
            query.execute("insert into focusrate(username,successResult,date) Values(%s,%s,%s)",(loguser,"YES",current_date))
            mydb.commit()
            messagebox.showinfo("Focus Mode", "Great job! Focus session complete.")


    
    def end_focus_mode():
        global session_ended_manually  
        session_ended_manually = True
        nonlocal haveYouOn
        if(not haveYouOn):
            messagebox.showinfo("Focus Mode", "You can't end something before its starts.")
            return

        show_taskbar()
        show_desktop_icons()
        haveYouOn = False
        current_date = datetime.now().strftime('%Y-%m-%d')
        query.execute("insert into focusrate(username,successResult,date) Values(%s,%s,%s)",(loguser,"NO",current_date))
        mydb.commit()
        messagebox.showinfo("Focus Mode", "Focus session has been manually ended")

    
    def browse_file():
        file = filedialog.askopenfilename()
        if file:
            appname.config(state='normal')
            appname.delete(0, END)
            appname.insert(0, file)
            appname.config(state='disabled')

    focusFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)
    activity = Label(focusFrame, text='Choose your activity : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    activity.place(x=170, y=80)
    appname = Entry(focusFrame, width=16, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 30, 'bold'))
    appname.place(x=520, y=78)
    appname.config(state='disabled')
    browseButton = Button(focusFrame, width=12, pady=7, text='Browse', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=browse_file).place(x=660, y=156)
    timer = Label(focusFrame, text='Set Timer (minutes) : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    timer.place(x=175, y=230)
    timerset = Entry(focusFrame, width=10, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 30, 'bold'))
    timerset.place(x=590, y=230)
    timer_label = Label(focusFrame, text="", font=("Helvetica", 14), fg="blue")
    modeonbutton = Button(focusFrame, width=12, pady=7, text='ON', borderwidth=3, bg='#32CD32', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=focus_on).place(x=260, y=396)
    modeoffbutton = Button(focusFrame, width=12, pady=7, text='OFF', borderwidth=3, bg='#DC143C', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=end_focus_mode).place(x=400, y=396)
    Idbutton = Button(focusFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)


comment = ""
timedata = ""


def remindermode():
    bgcolor(5)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')


    female_voice_found = False
    for voice in voices:
        if "female" in voice.name.lower() or "Zira" in voice.name or "Samantha" in voice.name:
            engine.setProperty('voice', voice.id)
            female_voice_found = True
            break

    if not female_voice_found and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)

    engine.setProperty('rate', 150)  

   
    reminder_active = False
    
    checkOn = False

    

    def reminder_on():
        global reminder_active
        nonlocal checkOn

    
        global comment , timedata
        comment = commentEntry.get().strip()
        timedata = timerEntry.get().strip()
        
        if not comment:
            messagebox.showerror("Reminder Set", "Remarks can't be blank")
            return
        if not all(x.isalpha() or x.isspace() for x in comment):
            messagebox.showerror("Error", "Remarks must contain only letters and spaces!")
            return
        if not timedata:
            messagebox.showerror("Error","Timeinput can't be blank")
            return
        if "." in timedata:
            messagebox.showerror("Error","Timeinput can't be Fraction")
            return
        if timedata.isdigit():
            if(int(timedata)==0):
                messagebox.showerror("Error","Timeinput should be greater than zero")
                return
            try:
                if not checkOn:
                    reminder_active = True
                    checkOn = True
                    minutes = int(timerEntry.get())
                    if minutes > 60:
                        messagebox.showinfo("Reminder Set", f"You will be reminded after {minutes//60} hour(s) and {minutes%60} minute(s).")
                    else:
                        messagebox.showinfo("Reminder Set", f"You will be reminded after {minutes} minutes.")
                else:
                    messagebox.showinfo("Reminder", "You have already ON this, if you want to renew the remider task then go and first turn off this task then come back!")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for the timer.")
                return
                
        else:
            messagebox.showerror("Error","Invalid TimeInput")
        
    
        def countdown():
            time.sleep(minutes * 60)  
            if reminder_active:
                while reminder_active:
                    engine.say(comment)
                    engine.runAndWait()
                    time.sleep(2)  
    
        threading.Thread(target=countdown, daemon=True).start()

    
    def reminder_off():
        global reminder_active
        nonlocal checkOn
        reminder_active = False
        checkOn = False
        engine.stop()
        

    
    reminderFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)
    commentLabel = Label(reminderFrame, text='Remark  : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    commentLabel.place(x=170, y=80)
    commentEntry = Entry(reminderFrame, width=18, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 32, 'bold'))
    commentEntry.place(x=365, y=74)
    commentEntry.insert(0, comment)
    timerLabel = Label(reminderFrame, text='Set Timer (minutes)  : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    timerLabel.place(x=175, y=230)
    timerEntry = Entry(reminderFrame, width=10, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 30, 'bold'))
    timerEntry.place(x=530, y=227)
    timerEntry.insert(0, timedata)
    remonbutton = Button(reminderFrame, width=12, pady=7, text='ON', borderwidth=3, bg='#32CD32', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=reminder_on).place(x=260, y=396)
    remoffbutton = Button(reminderFrame, width=12, pady=7, text='OFF', borderwidth=3, bg='#DC143C', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=reminder_off).place(x=400, y=396)
    Idbutton = Button(reminderFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)


current = ""

def musicmode():
    bgcolor(6)

    pygame.mixer.init()
    
    def music_on():
        selected_music = musicBox.get()
        if not selected_music:
            messagebox.showwarning("Warning", "Please select a music track before playing.")
            return
        global current
        current = selected_music
        music_files = {}
        query.execute("select title,musiclink from musiclist")
        musicli = query.fetchall()
        for title,link in musicli:
            music_files[title] = link
        print(music_files)
        
        pygame.mixer.music.load(music_files[selected_music])
        pygame.mixer.music.play(-1)  
    
    def music_off():
        pygame.mixer.music.stop()
    

    musicFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)
    musicLabel = Label(musicFrame, text='Select  Music  : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    musicLabel.place(x=170, y=80)
    musiclist = []
    query.execute("select title from musiclist")
    musictitles = query.fetchall()
    print(musictitles)
    for title in musictitles:
        musiclist.append(title[0])
    musicBox = ttk.Combobox(musicFrame,font=('broadway',25))
    musicBox['state'] = 'readonly'
    musicBox['values'] = musiclist
    musicBox.place(x=425, y=82)
    if current:
        musicBox.set(current)
    musiconbutton = Button(musicFrame, width=12, pady=7, text='ON', borderwidth=3, bg='#32CD32', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=music_on).place(x=260, y=396)
    musicoffbutton = Button(musicFrame, width=12, pady=7, text='OFF', borderwidth=3, bg='#DC143C', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=music_off).place(x=400, y=396)
    Idbutton = Button(musicFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)




def pomodoromode():
    
    bgcolor(4)

    stop_pomodoro = False
    pause_pomodoro = False
    checker = False

    def start_pomodoro():
        nonlocal stop_pomodoro, pause_pomodoro  
        stop_pomodoro = False 
        pause_pomodoro = False
        nonlocal checker 
        

        short_break = shortBreakEntry.get()
        if short_break.isdigit():
            if(int(short_break)==0):
                messagebox.showerror("Pomodoro Mode","Short Break values should be greater than 0")
                return
        else:
            messagebox.showerror("Pomodoro Mode","Invalid short break value")
            return

        long_break = longBreakEntry.get()
        if long_break.isdigit():
            if(int(long_break)==0):
                messagebox.showerror("Pomodoro Mode","long break values should be greater than 0")
                return
        else:
            messagebox.showerror("Pomodoro Mode","Invalid long break value")
            return

        shortBreakEntry.config(state='readonly')
        longBreakEntry.config(state='readonly')
        short_break = int(short_break) if short_break.isdigit() else 5
        long_break = int(long_break) if long_break.isdigit() else 30
        checker = True
        def countdown(duration, label_text):
            for remaining in range(duration, 0, -1):
                if stop_pomodoro:
                    return
                while pause_pomodoro:
                    time.sleep(1)  
                minutes, seconds = divmod(remaining, 60)
                CountdownLabel.config(text=f"{minutes:02d}:{seconds:02d}")
                root.update()
                time.sleep(1)

        for cycle in range(4):
            if stop_pomodoro:  
                return  

            messagebox.showinfo("Pomodoro", "Work for 25 minutes")
            countdown(25 * 60, "Work Time Remaining")
            if stop_pomodoro:
                return

            if cycle < 3: 
                messagebox.showinfo("Pomodoro", f"Take a short break of {short_break} minutes")
                countdown(short_break * 60, "Short Break Remaining")  
                if stop_pomodoro:
                    return
                while pause_pomodoro:
                    time.sleep(1)
                    

        if not stop_pomodoro:
            current_date = datetime.now().strftime('%Y-%m-%d')
            query.execute("INSERT INTO pomodoro (username, successResult, date) VALUES (%s, %s, %s)", (loguser, "YES", current_date))
            mydb.commit()
            messagebox.showinfo("Pomodoro", f"Session completed! Take a long break of {long_break} minutes")
            countdown(long_break * 60, "Long Break Remaining")
            if stop_pomodoro:
                return
            while pause_pomodoro:
                time.sleep(1)
                
    def pomo_on():
        threading.Thread(target=start_pomodoro, daemon=True).start()

    def pomo_stop():
        nonlocal pause_pomodoro, checker
        pause_pomodoro = not pause_pomodoro 
        if not checker:
            messagebox.showerror("Pomodoro Mode","You can't Pause/Resume without starting the pomodoro timer")
            return
        if not pause_pomodoro:
            pomostopbutton.config(text="PAUSE")
            messagebox.showinfo("Pomodoro", "Resumed Pomodoro session.")
        else:
            pomostopbutton.config(text="RESUME")
            messagebox.showinfo("Pomodoro", "Paused Pomodoro session.")

    def pomo_off():
        nonlocal stop_pomodoro , checker 
        stop_pomodoro = True
        if not checker:
            messagebox.showerror("Pomodoro Mode","You can't Turn OFF Timer without starting the pomodoro timer")
            return
        CountdownLabel.config(text="")
        checker = False
        current_date = datetime.now().strftime('%Y-%m-%d')
        query.execute("insert into pomodoro(username,successResult,date) Values(%s,%s,%s)", (loguser, "NO", current_date))
        mydb.commit()
        messagebox.showinfo("Pomodoro", "Pomodoro session manually stopped.")
        shortBreakEntry.config(state='normal')
        longBreakEntry.config(state='normal')

    def clear_entry(event):
        if event.widget.get() in ["5", "30"]:
            event.widget.delete(0, tk.END)

    def restore_default(event, default_value):
        if event.widget.get() == "":
            event.widget.insert(0, default_value)


    pomoFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)

    shortBreakLabel = Label(pomoFrame, text='Short Time Break (minutes)  : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    shortBreakLabel.place(x=170, y=80)
    shortBreakEntry = Entry(pomoFrame, width=4, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 30, 'bold'))
    shortBreakEntry.place(x=630, y=74)
    shortBreakEntry.insert(0, "5")
    shortBreakEntry.bind("<FocusIn>", clear_entry)
    shortBreakEntry.bind("<FocusOut>", lambda event: restore_default(event, "5"))
    shortBreakEntry.place(x=630, y=74)

    longBreakLabel = Label(pomoFrame, text='Long Time Break (minutes)  : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    longBreakLabel.place(x=170, y=230)
    longBreakEntry = Entry(pomoFrame, width=4, fg='black', border=1, bg="white", font=("Microsoft YaHei UI Light", 30, 'bold'))
    longBreakEntry.place(x=630, y=227)
    longBreakEntry.insert(0, "30")
    longBreakEntry.bind("<FocusIn>", clear_entry)
    longBreakEntry.bind("<FocusOut>", lambda event: restore_default(event, "30"))
    longBreakEntry.place(x=630, y=227)
    pomoonbutton = Button(pomoFrame, width=12, pady=7, text='ON', borderwidth=3, bg='#32CD32', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=pomo_on).place(x=210, y=396)
    pomostopbutton = Button(pomoFrame, width=12, pady=7, text='PAUSE', borderwidth=3, bg='#00008B', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#00008B", activeforeground="#FFFFFF", command=pomo_stop)
    pomostopbutton.place(x=350, y=396)
    pomoffbutton = Button(pomoFrame, width=12, pady=7, text='OFF', borderwidth=3, bg='#DC143C', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=pomo_off).place(x=490, y=396)
    Idbutton = Button(pomoFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)
    CountdownLabel = Label(pomoFrame, text='', fg='#00FFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 60, 'bold'))
    CountdownLabel.place(x=680, y=350)

currentgame = ""

def gamemode():

    bgcolor(7)
    query.execute("select title,gamelink from gamelist")
    gamedata = query.fetchall()
    gamefiles = []
    gamelinkfiles = []
    
    for title,gamelink in gamedata:
        gamefiles.append(title)
        gamelinkfiles.append(gamelink)
    


    def play_game():
        selected_game = musicBox.get()
        global currentgame
        currentgame = selected_game
        if not selected_game:
            messagebox.showwarning("Warning", "Please select a Game before playing.")
            return
        else:
            loc = None
            for i in range(0,len(gamefiles)):
                if(gamefiles[i]==selected_game):
                    loc = i
            path = gamelinkfiles[loc]
            subprocess.run(["python", path])


    musicFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)
    musicLabel = Label(musicFrame, text='Select  Game  : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    musicLabel.place(x=170, y=80)
    musiclist = ["TIC TAC TOE","LUDO","CAR RACING","GUESS THE NUMBER"]
    musicBox = ttk.Combobox(musicFrame,font=('broadway',25))
    musicBox['state'] = 'readonly'
    musicBox['values'] = gamefiles
    musicBox.place(x=425, y=82)
    if currentgame:
        musicBox.set(currentgame)
    musicoffbutton = Button(musicFrame, width=20, pady=7, text='PLAY', borderwidth=3, bg='#DC143C', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 15, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=play_game).place(x=380, y=370)
    Idbutton = Button(musicFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=5)





def analysismode():
    bgcolor(8)
    current_date = datetime.now().strftime('%Y-%m-%d')
    Fdate = current_date
    tdate = current_date
    
    query.execute("select count(*) from blacklist where username=%s and date between %s and %s",(loguser,Fdate,tdate))
    BlackTotal = query.fetchone()[0]
    
    query.execute("select count(*) from whitelist where username=%s and date between %s and %s",(loguser,Fdate,tdate))
    WhiteTotal = query.fetchone()[0]

    query.execute("SELECT COUNT(*) FROM pomodoro WHERE username = %s and date between %s and %s",(loguser,Fdate,tdate))
    PomoTotal = query.fetchone()[0]
    query.execute("SELECT COUNT(*) FROM pomodoro WHERE username = %s and date between %s and %s and successResult=%s",(loguser,Fdate,tdate,"YES"))
    PomoYES = query.fetchone()[0]
    if PomoTotal > 0:
        PomoSuccess = (PomoYES / PomoTotal) * 100 
    else:
        PomoSuccess = 0  

    query.execute("SELECT COUNT(*) FROM focusrate WHERE username = %s and date between %s and %s",(loguser,Fdate,tdate))
    focusTotal = query.fetchone()[0]
    query.execute("SELECT COUNT(*) FROM focusrate WHERE username = %s and date between %s and %s and successResult=%s",(loguser,Fdate,tdate,"YES"))
    focusYES = query.fetchone()[0]
    if focusTotal > 0:
        focusSuccess = (focusYES / focusTotal) * 100
    else:
        focusSuccess = 0  

    
    query.execute("select website from whitelist where username=%s and date Between %s and %s",(loguser,Fdate,tdate))
    WhitewebsiteItems = query.fetchall()

    query.execute("select website from blacklist where username=%s and date Between %s and %s",(loguser,Fdate,tdate))
    BlackwebsiteItems = query.fetchall()

   

    def check_analysis():
        nonlocal Fdate
        nonlocal tdate
        nonlocal BlackTotal
        nonlocal WhiteTotal
        nonlocal PomoYES
        nonlocal PomoTotal
        nonlocal PomoSuccess
        nonlocal focusYES
        nonlocal focusTotal
        
        nonlocal focusSuccess
        nonlocal WhitewebsiteItems
        nonlocal BlackwebsiteItems

        Fdate = Fromcal.get_date()
        tdate = Tocal.get_date()

        if not Fdate:
            messagebox.showerror("Analysis","From Date should not be blank")
            return
        if not tdate:
            messagebox.showerror("Analysis","To Date should not be blank")
            return
        current_date = date.today()
        if (Fdate>current_date or tdate>current_date):
            messagebox.showerror("Analysis","Invalid Date")
            return



        if(tdate>=Fdate):
            query.execute("select count(*) from blacklist where username=%s and date between %s and %s",(loguser,Fdate,tdate))
            BlackTotal = query.fetchone()[0]
            Blacklistans.config(text=BlackTotal)

            query.execute("select count(*) from whitelist where username=%s and date between %s and %s",(loguser,Fdate,tdate))
            WhiteTotal = query.fetchone()[0]
            Whiteans.config(text=WhiteTotal)

            query.execute("SELECT COUNT(*) FROM pomodoro WHERE username = %s and date between %s and %s",(loguser,Fdate,tdate))
            PomoTotal = query.fetchone()[0]
            query.execute("SELECT COUNT(*) FROM pomodoro WHERE username = %s and date between %s and %s and successResult=%s",(loguser,Fdate,tdate,"YES"))
            PomoYES = query.fetchone()[0]
           
            if PomoTotal > 0:
                PomoSuccess = (PomoYES / PomoTotal) * 100
            else:
                PomoSuccess = 0  

            if(PomoSuccess<=24):
                Pomoans.config(text=f"{PomoSuccess:.1f}%",fg="#8B0000")
            elif(PomoSuccess<=49):
                Pomoans.config(text=f"{PomoSuccess:.1f}%",fg="#FF8C00")
            elif(PomoSuccess<=74):
                Pomoans.config(text=f"{PomoSuccess:.1f}%",fg="#FFDF00")
            else:
                Pomoans.config(text=f"{PomoSuccess:.1f}%",fg="#90EE90")
        

            query.execute("SELECT COUNT(*) FROM focusrate WHERE username = %s and date between %s and %s",(loguser,Fdate,tdate))
            focusTotal = query.fetchone()[0]
            query.execute("SELECT COUNT(*) FROM focusrate WHERE username = %s and date between %s and %s and successResult=%s",(loguser,Fdate,tdate,"YES"))
            focusYES = query.fetchone()[0]
           
            if focusTotal > 0:
                focusSuccess = (focusYES / focusTotal) * 100
            else:
                focusSuccess = 0 

            if(focusSuccess<=24):
                focusans.config(text=f"{focusSuccess:.1f}%",fg="#8B0000")
            elif(focusSuccess<=49):
                focusans.config(text=f"{focusSuccess:.1f}%",fg="#FF8C00")
            elif(focusSuccess<=74):
                focusans.config(text=f"{focusSuccess:.1f}%",fg="#FFDF00")
            else:
                focusans.config(text=f"{focusSuccess:.1f}%",fg="#90EE90")

            query.execute("select website from blacklist where username=%s and date Between %s and %s",(loguser,Fdate,tdate))
            BlackwebsiteItems = query.fetchall()
            query.execute("select website from whitelist where username=%s and date Between %s and %s",(loguser,Fdate,tdate))
            WhitewebsiteItems = query.fetchall()
        else:
            messagebox.showerror("Incorrect Date Selection", "Please select the range of date correctly")
    
    new_windowb = None
    def view_Blacklist():
        nonlocal new_windowb
        if new_windowb is not None and new_windowb.winfo_exists():
            new_windowb.destroy()
        nonlocal BlackwebsiteItems
        new_windowb = Toplevel(root)  
        new_windowb.title("Blacklist Websites")
        new_windowb.iconbitmap("logo.ico")
        new_windowb.geometry("350x250+570+330")
        new_windowb.resizable(False,False)
        v_scrollbar = Scrollbar(new_windowb, orient=VERTICAL)
        h_scrollbar = Scrollbar(new_windowb, orient=HORIZONTAL)
        weblist = Listbox(new_windowb, width=23, height=8, bg='#24344F', fg='#FFFFFF', 
                                font=("Microsoft YaHei UI Light", 20, 'bold'), selectmode=SINGLE,yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        weblist.place(x=0, y=0)
        v_scrollbar.config(command=weblist.yview)
        h_scrollbar.config(command=weblist.xview)

        v_scrollbar.place(x=23, y=0, height=220)  
        h_scrollbar.place(x=0, y=8, width=330) 
        
        query.execute("select website from blacklist where username=%s and date Between %s and %s",(loguser,Fdate,tdate))
        websiteItems = query.fetchall()

        for item in websiteItems:
                weblist.insert(END, item)


    new_window = None
    def view_Whitelist():
        nonlocal new_window
        if new_window is not None and new_window.winfo_exists():
            new_window.destroy()
        new_window = Toplevel(root)  
        new_window.title("Whitelist Websites")
        new_window.iconbitmap("logo.ico")
        new_window.geometry("350x250+570+330")
        new_window.resizable(False,False)
        v_scrollbar = Scrollbar(new_window, orient=VERTICAL)
        h_scrollbar = Scrollbar(new_window, orient=HORIZONTAL)
        weblist = Listbox(new_window, width=23, height=8, bg='#24344F', fg='#FFFFFF', 
                                font=("Microsoft YaHei UI Light", 20, 'bold'), selectmode=SINGLE,yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        weblist.place(x=0, y=0)
        v_scrollbar.config(command=weblist.yview)
        h_scrollbar.config(command=weblist.xview)

        v_scrollbar.place(x=23, y=0, height=220)  
        h_scrollbar.place(x=0, y=8, width=330) 
        
        query.execute("select website from whitelist where username=%s and date Between %s and %s",(loguser,Fdate,tdate))
        websiteItems = query.fetchall()

        for item in websiteItems:
                weblist.insert(END, item)

        

    def send_Email():
         
        nonlocal Fdate
        nonlocal tdate
        nonlocal BlackTotal
        nonlocal WhiteTotal
        nonlocal PomoYES
        nonlocal PomoTotal
        nonlocal PomoSuccess
        nonlocal focusYES
        nonlocal focusTotal
        nonlocal focusSuccess
        nonlocal WhitewebsiteItems
        nonlocal BlackwebsiteItems
        
        SENDER_EMAIL = "aniketsingh18pd@gmail.com"
        SENDER_PASSWORD = "lwskzckalenfatzk" 
        query.execute("select email from user where username=%s",(loguser,))
        RECEIVER_EMAIL = query.fetchone()[0]

        subject = "Report From " + str(Fdate) + " to " + str(tdate)
        body = f"Hello {name}, as per your request, we are sending you a report of your performance and other details " \
        f"from {Fdate} to {tdate}.....\n\nYou have Blacklisted total {BlackTotal} websites."

        if BlackwebsiteItems:
            body = body + "which are "
            for item in BlackwebsiteItems:
                body = body + str(item[0]) + ", "
        else:
            body = body

        body = body + "and You have Whitelisted total " + str(WhiteTotal) + " websites "
        if WhitewebsiteItems:
            body = body + "which are "
            for item in WhitewebsiteItems:
                body = body + str(item[0]) + ", "
        else:
            body = body

        body = body + ". Your focus sucessrate is " + str(focusSuccess)[0:4] + "% which is "

        focusSuccess = float(focusSuccess)
        if(focusSuccess<=24):
            body = body + " poor. you need to put in serious effort and work much harder to improve! "
        elif(focusSuccess<=49):
            body = body + " medicore. There is plenty of room for improvement , so keep pushing forward! "
        elif(focusSuccess<=74):
            body = body + " good. You are on right track-keep up the effort to reach excellence! "
        elif(focusSuccess<=100):
            body = body + " excellent! Outstanding work-keep striving for even greater success! "

        body = body + " Your pomodoro successrate is "+ str(PomoSuccess)[0:4] + "% which is "
        PomoSuccess = float(PomoSuccess)
        if(PomoSuccess<=24):
            body = body + " poor. Significant improvemnet is needed-push yourself harder to get better result! "
        elif(PomoSuccess<=49):
            body = body + " medicore. Progress is possible with more dedication and effort! "
        elif(PomoSuccess<=74):
            body = body + " good. Keep up the momentum and strive for even greater achievements! "
        elif(PomoSuccess<=100):
            body = body + " excellent! Keep pushing your limits and continue excelling! "

        
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            messagebox.showinfo("Sucess!", "Email has been sent successfully!")
        except Exception as e:
            messagebox.showerror("Failed!", "Email has been not sent, please try again!")
        finally:
            server.quit()



    analysisFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)
    datelabel = Label(analysisFrame, text='Select Date  : ', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    datelabel.place(x=175, y=44)
    Fromcal = DateEntry(analysisFrame, width=7, background='darkblue', foreground='white',state='readonly', borderwidth=2,font=('Microsoft YaHei UI Light', 20, 'bold'))
    Fromcal.place(x = 400, y=48)
    tolabel = Label(analysisFrame, text='to', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 20, 'bold'))
    tolabel.place(x=557, y=47)
    Tocal = DateEntry(analysisFrame, width=7, background='darkblue', foreground='white',state='readonly', borderwidth=2,font=('Microsoft YaHei UI Light', 20, 'bold'))
    Tocal.place(x=614, y=48)
    Idbutton = Button(analysisFrame,width=20,pady=7,text=loguser,borderwidth=0,bg='#0f172a',fg='#00CDFE',cursor='hand2',border=0,font=("Microsoft YaHei UI Light", 12, "bold"), activebackground="#0f172a", activeforeground="#00CDFE",command=profile).place(x=710,y=2)
    onbutton = Button(analysisFrame, width=6, pady=7, text='OK', borderwidth=3, bg='#DC143C', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 8, "bold"), activebackground="#DC143C", activeforeground="#FFFFFF", command=check_analysis)
    onbutton.place(x=790, y=52)
     
    BlacklistL = Label(analysisFrame, text='Total Blacklist Website   :', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    BlacklistL.place(x=200, y=145)
    Blacklistans = Label(analysisFrame, text=BlackTotal, fg='#00CDEF', bg='#0f172a', font=('Microsoft YaHei UI Light', 28, 'bold'))
    Blacklistans.place(x=640, y=145)
    viewR = Button(analysisFrame, width=20, pady=7, text='view website', borderwidth=3, bg='#0f172a', fg='#FF8C00', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 12, "bold"),activebackground="#0f172a", activeforeground="#FF8C00",command=view_Blacklist)
    viewR.place(x=730, y=145)
    
    WhitelistL = Label(analysisFrame, text='Total Whitelist Website  :', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 25, 'bold'))
    WhitelistL.place(x=200, y=225)
    Whiteans = Label(analysisFrame, text=WhiteTotal, fg='#00CDEF', bg='#0f172a', font=('Microsoft YaHei UI Light', 28, 'bold'))
    Whiteans.place(x=640, y=225)
    viewW = Button(analysisFrame, width=20, pady=7, text='view website', borderwidth=3, bg='#0f172a', fg='#FF8C00', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 12, "bold"),activebackground="#0f172a", activeforeground="#FF8C00",command=view_Whitelist)
    viewW.place(x=730, y=225)

    sendMail = Button(analysisFrame, width=20, pady=7, text='SEND REPORT TO EMAIL', borderwidth=3, bg='#DC143C', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 10, "bold"), activebackground="#DC143C", activeforeground="#FFFFFF", command=send_Email)
    sendMail.place(x=295, y=450)

    pomoL = Label(analysisFrame, text='Pomodoro Success rate   :', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    pomoL.place(x=200, y=305)
    Pomoans = Label(analysisFrame, text=PomoSuccess, fg='#00CDEF', bg='#0f172a', font=('Microsoft YaHei UI Light', 28, 'bold'))
    Pomoans.place(x=640, y=305)
    if(PomoSuccess<=24):
        Pomoans.config(text=f"{PomoSuccess:.1f}%",fg="#8B0000")
    elif(PomoSuccess<=49):
        Pomoans.config(text=f"{PomoSuccess:.1f}%",fg="#FF8C00")
    elif(PomoSuccess<=74):
        Pomoans.config(text=f"{PomoSuccess:.1f}%",fg="#FFDF00")
    else:
        Pomoans.config(text=f"{PomoSuccess:.1f}%",fg="#90EE90")
    

    focusL = Label(analysisFrame, text='Focusmode Sucess rate   :', fg='#FFFFFF', bg='#0f172a', font=('Microsoft YaHei UI Light', 24, 'bold'))
    focusL.place(x=200, y=385)
    focusans = Label(analysisFrame, text=focusSuccess, fg='#00CDEF', bg='#0f172a', font=('Microsoft YaHei UI Light', 28, 'bold'))
    focusans.place(x=640, y=385)
    if(focusSuccess<=24):
        focusans.config(text=f"{focusSuccess:.1f}%",fg="#8B0000")
    elif(focusSuccess<=49):
        focusans.config(text=f"{focusSuccess:.1f}%",fg="#FF8C00")
    elif(focusSuccess<=74):
        focusans.config(text=f"{focusSuccess:.1f}%",fg="#FFDF00")
    else:
        focusans.config(text=f"{focusSuccess:.1f}%",fg="#90EE90")
    


    
Blacklist = Button(root, width=12, pady=7, text='Restrict Site', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF", command=blockweb)
Blacklist.place(x=17, y=62)
Whitelist = Button(root, width=12, pady=7, text='Whitelist', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=whitelistweb)
Whitelist.place(x=17, y=117)
FocusButton = Button(root, width=12, pady=7, text='Focus', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=focusmode)
FocusButton.place(x=17, y=170)
Pomodoro = Button(root, width=12, pady=7, text='Pomodoro', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=pomodoromode)
Pomodoro.place(x=17, y=223)
Reminder = Button(root, width=12, pady=7, text='Reminder', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=remindermode)
Reminder.place(x=17, y=276)
Music = Button(root, width=12, pady=7, text='Music', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=musicmode)
Music.place(x=17, y=329)
Game = Button(root, width=12, pady=7, text='Game', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=gamemode)
Game.place(x=17, y=382)
Analysis = Button(root, width=12, pady=7, text='Analytics', borderwidth=3, bg='#FF8C00', fg='#FFFFFF', cursor='hand2', border=0, font=("Microsoft YaHei UI Light", 9, "bold"), activebackground="#FF8C00", activeforeground="#FFFFFF",command=analysismode)
Analysis.place(x=17, y=435)


def profile():
    ProfileFrame = Frame(CFrame, width=785, height=500, bg='#0f172a').place(x=140, y=0)

    userprofile = Label(ProfileFrame, text="User-Profile", fg='#FF8C00', bg='#0f172a', font=('Microsoft YaHei UI Light', 28, 'bold'))
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
    
    Blacklist.config(background="#FF8C00")
    Whitelist.config(background="#FF8C00")
    FocusButton.config(background="#FF8C00")
    Pomodoro.config(background="#FF8C00")
    Reminder.config(background="#FF8C00")
    Music.config(background="#FF8C00")
    Game.config(background="#FF8C00")
    Analysis.config(background="#FF8C00")

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
            query.execute("update user set name=%s, email=%s, password=%s where username=%s", (nameU, emailU, hashed_password,usnU))
            mydb.commit()
            global name,email,userPassword

            name = nameU
            email = emailU
            userPassword = passU
            
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
        passwoEntry.insert(0,userPassword)
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

