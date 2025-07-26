from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import  Tk, Canvas
from PIL import Image, ImageTk
import mysql.connector
import os

root = Tk()
root.geometry("1150x764")
root.title("Poll Admin")

admin_id = StringVar()
username = StringVar()
password = StringVar()
securityQuestion = StringVar()

connect = mysql.connector.connect(
      host = "localhost",
      user = "root",
      password = "412356",
      database = "secure_vote_db"
  )

if(connect.is_connected()):
  cursor = connect.cursor()

def security_question_popup():
  messagebox.showinfo("Authentication","You can enter either password or Security Question.\nPlease enter the password OR the answer for the security question you have given in registration")

def login():
  admin_id_fetch = admin_id.get().strip()
  username_fetch = username.get().strip()
  password_fetch = password.get().strip()
  securityQ_fetch = securityQuestion.get().strip()
  
  if(admin_id_fetch == "" or username_fetch == ""):
    messagebox.askretrycancel("Retry","Please fill the all the fields to log in")
  else:
    if(securityQ_fetch == ""):
      query = "SELECT username, password FROM poll_admin WHERE admin_id = %s"
      cursor.execute(query, (admin_id_fetch,))
      result = cursor.fetchone()

      if(result[0] == username_fetch and result[1] == password_fetch):
        messagebox.showinfo("Success","Login Successful")
        
        cursor.close()
        connect.close()

        os.startfile("Poll2.py")
        
        root.destroy()
      else:
        messagebox.showinfo("Failed","Login Unsuccessful, please check your credentials")

    if(password_fetch == ""):
      query = "SELECT username, security_question FROM poll_admin WHERE admin_id = %s"
      cursor.execute(query, (admin_id_fetch,))
      result = cursor.fetchone()

      if(result[0] == username_fetch and result[1] == securityQ_fetch):
        messagebox.showinfo("Success","Login Successful")

        cursor.close()
        connect.close()

        os.startfile("Poll2.py")
        
        root.destroy()
      else:
        messagebox.showinfo("Failed","Login Unsuccessful, please check your credentials")

  
canvas = Canvas(root, width=1150, height=764)
canvas.pack(fill = "both", expand = True)

image = Image.open("BACKGROUND-Poll1.png")
photo = ImageTk.PhotoImage(image)

canvas.create_image(0, 0, anchor = "nw", image=photo)

Label(root, text = "LOGIN", font = ("Tahoma", 16), bg = "white").place(x = 555, y = 330)

Label(root, text = "Admin ID:", font = ("Tahoma", 12), bg = "white").place(x = 435, y = 380)
admin_entry = Entry(root, textvariable = admin_id, font = ("Tahoma", 12), bg = "white smoke").place(x = 560, y = 380)

Label(root, text = "Username:", font = ("Tahoma", 12), bg = "white").place(x = 435, y = 410)
username_entry = Entry(root, textvariable = username, font = ("Tahoma", 12), bg = "white smoke").place(x = 560, y = 410)

Label(root, text = "Password:", font = ("Tahoma", 12), bg = "white").place(x = 435, y = 440)
passwd_entry = Entry(root, textvariable = password, font = ("Tahoma", 12), bg = "white smoke", show = "*").place(x = 560, y = 440)

Label(root, text = "Security Question:",font = ("Tahoma", 12), bg = "white").place(x = 420, y = 470)
securityQ_entry = Entry(root, textvariable = securityQuestion, font = ("Tahoma", 12), bg = "white smoke").place(x = 560, y = 470)

securityQ_button = Button(root, text = "�", font = ("Calibri", 8), command = security_question_popup).place(x = 750, y = 470)

login_button = Button(root, text = "  →  ", font = ("Tahoma", 14), bg = "PaleTurquoise2", command = login).place(x = 555, y = 530)
                      
root.mainloop()
