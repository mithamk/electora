from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import pickle
import os
import ast
import ssl

SERVER_HOST = "MSB"
SERVER_PORT = 12345

root = Tk()
root.geometry("1150x764")
root.title("Voter")

voter_id = StringVar()
email = StringVar()
phone_number = StringVar()
email_otp_entry = StringVar()
phno_otp_entry = StringVar()

def submit_vote(candidate_str):
    if candidate_str:
        try:
            candidate_str = ast.literal_eval(candidate_str)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            ssl_client_socket = context.wrap_socket(client_socket)
            ssl_client_socket.connect((SERVER_HOST, SERVER_PORT))

            vote = {"voter_id": voter_id.get().strip(), "vote": candidate_str}
            ssl_client_socket.send(pickle.dumps(vote))

            response = pickle.loads(ssl_client_socket.recv(4096))
            
            if(response.get("status") == "ended"):
                messagebox.showinfo("⏳","The poll has ended.")
            if(response.get("status") == "vote_received"):
                messagebox.showinfo("Success", "Your vote has been recorded successfully!\nPoll End Time: At or Before 5:00 PM IST.\nThe poll results shall be sent via registered email.\n\nNote: If you don't find the email in your inbox, please check your spam folder.")
                os.startfile("voter.py")
                root.destroy()
            else:
                messagebox.showerror("❌ Error", "Failed to cast vote")
            ssl_client_socket.close()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Server error: {e}")
    else:
        messagebox.showinfo("⛔ Error", "Please select a candidate before voting.")

def display_poll(poll_info):
    poll_window = Toplevel(root)
    poll_window.title("Poll")
    poll_window.geometry("1150x764")

    canvas = Canvas(poll_window, width=1150, height=764)
    canvas.pack(fill="both", expand=True)

    image = Image.open("BACKGROUND-Poll.png")
    poll_window.bg_photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=poll_window.bg_photo)

    selected_option = StringVar()
    selected_option.set(None)

    print(poll_info)

    y = 243

    for i in poll_info:
        if i["symbol"] == 'π - PPP':
            option_text = i["symbol"][0] + "  " + i["symbol"][-3:]
        else:
            option_text = i["symbol"][0] + " " + i["symbol"][-3:]
        option = Radiobutton(poll_window, 
                             text = option_text, 
                             variable = selected_option, 
                             value = str(i), 
                             font = ("Tahoma", 30), 
                             bg = "white")
        option.place(x = 500, y = y) 
        y = y + 50

    submit_button = Button(poll_window, text = "  Vote  ", command = lambda:submit_vote(selected_option.get()), font = ("Tahoma", 16))
    submit_button.place(x = 500, y = y + 40)

def verify_otp(expected_otp):
    """Check if entered OTP matches the one received"""
    if email_otp_entry.get().strip() == expected_otp[0] and phno_otp_entry.get().strip() == expected_otp[1]:
        messagebox.showinfo("✅ Success", "OTP Verified! Access Granted.")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
            
        ssl_client_socket = context.wrap_socket(client_socket)
        ssl_client_socket.connect((SERVER_HOST, SERVER_PORT))
        ssl_client_socket.send(pickle.dumps({"authenticated": True}))
        
        data = pickle.loads(ssl_client_socket.recv(4096))
        ssl_client_socket.close()

        root.withdraw()

        if(data.get("status") == "success"):
            if(data["poll_info"] == -1):
                messagebox.showinfo("⏳","The poll has ended.")
            else:
                poll_info = data["poll_info"]
                display_poll(poll_info)
        else:
            messagebox.showerror("❌", "Error displaying Poll")
        otp_window.destroy()
    else:
        messagebox.showerror("❌ Error", "Incorrect OTP! Please try again.")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        ssl_client_socket = ssl.wrap_socket(client_socket)
        ssl_client_socket.connect((SERVER_HOST, SERVER_PORT))
        ssl_client_socket.send(pickle.dumps({"authenticated": False}))
        ssl_client_socket.close()

def login():
    """Send voter data to the server and request OTP"""
    if voter_id.get().strip() and email.get().strip() and phone_number.get().strip():
        voter_data = {
            'voter_id': voter_id.get().strip(),
            'email': email.get().strip(),
            'phone_number': phone_number.get().strip()
        }
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
            
        ssl_client_socket = context.wrap_socket(client_socket)
        ssl_client_socket.connect((SERVER_HOST, SERVER_PORT))

        request_data = {"check_voter": voter_data}
        ssl_client_socket.send(pickle.dumps(request_data))

        # Receive response from server
        flag = pickle.loads(ssl_client_socket.recv(4096))
        ssl_client_socket.close()
        
        print(flag)

        if flag == 1:
            messagebox.showinfo("🗳️", "Voting completed for this voter.\nPoll End Time: At or Before 5:00 PM IST.\nThe poll results shall be sent via registered email.\n\nNote: If you don't find the email in your inbox, please check your spam folder.")
            return
        if flag == 0:
            messagebox.showinfo("❌", "Voter Not Found! Access Denied")
            return
        if flag == -2:
            messagebox.showinfo("⏳","The poll has ended.")
            return
        if flag is not None:  # Server should return a OTP
            messagebox.showinfo("✅", "Voter Found! OTP Sent to Registered Email ID and Phone Number.\n\nNote: If you don't find the email in your inbox, please check your spam folder.")

            # OTP Entry Box UI
            global otp_window
            otp_window = Toplevel(root)
            otp_window.title("OTP Verification")
            otp_window.geometry("325x325+100+50")
            Label(otp_window, text="Enter email OTP: ", font=("Tahoma", 14)).pack(pady=20)
            Entry(otp_window, textvariable=email_otp_entry, font=("Tahoma", 12), bg="white smoke").pack(pady=10)
            Label(otp_window, text="Enter phone OTP: ", font=("Tahoma", 14)).pack(pady=20)
            Entry(otp_window, textvariable=phno_otp_entry, font=("Tahoma", 12), bg="white smoke").pack(pady=10)
            Button(otp_window, text="  ✅  ", font=("Tahoma", 12), bg="PaleTurquoise2", command=lambda: verify_otp(flag)).pack(pady=20)
            
        else:
            messagebox.showinfo("❌", "Unexpected Error Occured. Please try again later")

    else:
        messagebox.showerror("Error", "Please fill in all fields to log in.")

# UI Components
canvas = Canvas(root, width=1150, height=764)
canvas.pack(fill="both", expand=True)

image = Image.open("BACKGROUND-Poll1.png")
photo = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor="nw", image=photo)

Label(root, text="LOGIN", font=("Tahoma", 16), bg="white").place(x=555, y=317)
Label(root, text="Voter ID:", font=("Tahoma", 12), bg="white").place(x=435, y=380)
Entry(root, textvariable=voter_id, font=("Tahoma", 12), bg="white smoke").place(x=560, y=380)
Label(root, text="Email:", font=("Tahoma", 12), bg="white").place(x=435, y=410)
Entry(root, textvariable=email, font=("Tahoma", 12), bg="white smoke").place(x=560, y=410)
Label(root, text="Phone Number:", font=("Tahoma", 12), bg="white").place(x=435, y=442)
Entry(root, textvariable=phone_number, font=("Tahoma", 12), bg="white smoke").place(x=560, y=442)
Button(root, text="  →  ", font=("Tahoma", 12), bg="PaleTurquoise2", command=login).place(x=555, y=500)

root.mainloop()
