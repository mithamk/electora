from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import  Tk, Canvas
from PIL import Image, ImageTk
from tkinter import PhotoImage
import socket
import pickle
import os
import csv
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
from datetime import date

root = Tk()
root.geometry("1150x764")
root.title("Poll Admin")

no_of_candidates = StringVar()

images = ["♞ - KJP",
          "✪ - SAP",
          "✏ - PVP",
          "☎ - CCP",
          "❇ - PSP",
          "π - PPP",
          "ↂ - TFP",
          "≙ - ERM"]

image_vars = []
names = []

poll_time = "17:00"

def display_glossary():
  def remove():
    label.destroy()
    button.destroy()
    
  image = PhotoImage(file = "grid.png")
  
  label = Label(root, image = image, height = 190, width = 300)
  label.image = image
  label.place(x = 848, y = 30)

  button = Button(root, text = "⛝", command = remove, bg = "white")
  button.place(x = 1127, y = 30)

def end_poll(WINNER):
  if(WINNER is None or WINNER == [] or len(WINNER) == 0):
    message.showinfo("No winners","No winners have emerged from the poll. The poll administrator is advised to take appropriate steps to inform the voters accordingly.")
  else:
    if(len(WINNER) == 1):
      winner = WINNER[0]
    else:
      winner = WINNER
    text = f"""\
    This is to officially declare that {winner} has secured the highest number of votes and is hereby announced as the elected winner of the poll.
    We extend our sincere appreciation to all voters for their active participation and commitment to upholding democratic values.
    For records and verification, this result has been digitally signed and time-stamped by the Electoral Committee.
    © 2025 Electora Voting Authority. All rights reserved.
    """

    html = f"""
        <!DOCTYPE html>
        <html>
          <head>
            <style>
              @keyframes fadeInUp {{
                from {{
                  opacity: 0;
                  transform: translateY(20px);
                }}
                to {{
                  opacity: 1;
                  transform: translateY(0);
                }}
              }}
            
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
            body {{
              margin: 0;
              padding: 0;
              font-family: 'Poppins', sans-serif;
              background: url('confetti.gif') 
              background-size: cover;
            }}
            .email-container {{
              animation: fadeInUp 1s ease-out;
              background-color: #ffffff;
              border-radius: 25px;
              width: 600px;
              margin: 40px auto;
              padding: 40px;
              box-shadow: 0 6px 25px rgba(0,0,0,0.15);
            }}
          /*.logo {{
            margin-bottom: 20px;
          }}*/
          .header {{
            color: #0a3d62;
            font-size: 28px;
            font-weight: 600;
          }}
          .subtitle {{
            color: #34495e;
            font-size: 14px;
            margin-bottom: 20px;
          }}
          .divider {{
            border: none;
            height: 3px;
            background-color: #0a3d62;
            margin: 20px 0;
            border-radius: 5px;
          }}
          .content {{
            color: #2c3e50;
            font-size: 17px;
            line-height: 1.7;
          }}
          .highlight {{
            color: #3498db;
            font-weight: 600;
          }}
          .footer {{
            color: #3498db;
            font-size: 15px;
            margin-top: 25px;
          }}
        </style>
        <style>
        .cta-button {{
          background-color: #3498db;
          color: #fff;
          padding: 15px 30px;
          font-size: 18px;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          animation: bounce 1.5s infinite;
          box-shadow: 0 0 10px #3498db, 0 0 20px #3498db;
          transition: transform 0.2s;
        }}

        @keyframes bounce {{
          0%, 100% {{transform: translateY(0); }}
          50% {{transform: translateY(-10px); }}
        }}

        .reveal-text {{
          opacity: 0;
          transform: translateY(20px);
          animation: slideFadeIn 1s ease-out forwards;
        }}

        @keyframes slideFadeIn {{
          to {{
            opacity: 1;
            transform: translateY(0);
          }}
        }}
      </style>
    </head>
    <body>
      <style>
        .sparkle {{
          position: absolute;
          width: 8px;
          height: 8px;
          background: radial-gradient(circle, #ffffff 0%, #00d2ff 70%);
          border-radius: 50%;
          animation: floatSparkle 6s infinite ease-in-out;
          opacity: 0.8;
        }}

        @keyframes floatSparkle {{
          0% {{
            transform: translateY(0) scale(1);
            opacity: 0.8;
          }}
          50% {{
            transform: translateY(-20px) scale(1.2);
            opacity: 0.5;
          }}
          100% {{
            transform: translateY(0) scale(1);
            opacity: 0.8;
          }}
        }}

        .sparkle:nth-child(1) {{ top: 30px; left: 50px; animation-delay: 0s; }}
        .sparkle:nth-child(2) {{ top: 80px; left: 300px; animation-delay: 1s; }}
        .sparkle:nth-child(3) {{ top: 150px; left: 500px; animation-delay: 2s; }}
        .sparkle:nth-child(4) {{ top: 220px; left: 200px; animation-delay: 3s; }}
      </style>
    <div class="sparkle"></div><div class="sparkle"></div><div class="sparkle"></div><div class="sparkle"></div>
    <div class="email-container">
      <div align="center" class="logo">
      <img style = "width: 150px; height: 150px" src = "cid:LOGO">
      </div>
      <div align="center" class="header reveal-text">Electora Voting Authority</div>
      <div align="center" class="subtitle">Verified • Trusted • Safe</div>
      <hr class="divider">
      <div class="content">
        <p>This is to officially declare that <strong>{winner}</strong> has secured the highest number of votes and is hereby announced as the elected winner of the poll.</p>
        <p class="highlight">We extend our sincere appreciation to all voters for their active participation and commitment to upholding democratic values.</p>
        <p class="footer">For records and verification, this result has been digitally signed and time-stamped by the Electoral Committee.<br><p style = "text-align: center; font-size: 12px; color: #555; margin-top: 30px; border-top: 1px solid #ccc; padding-top: 10px;">© 2025 Electora Voting Authority. All rights reserved.</p></p>
      </div>
    </div>
<canvas id="confetti-canvas" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:999;"></canvas>
<script>
(function() {{
  const canvas = document.getElementById("confetti-canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const pieces = [];
  for (let i = 0; i < 150; i++) {{
    pieces.push({{
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height - canvas.height,
      size: Math.random() * 10 + 5,
      speed: Math.random() * 3 + 2,
      color: `hsl(${{Math.random() * 360}}, 100%, 70%)`,
      rotation: Math.random() * 360,
    }});
  }}

  let animationId;

  function update() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pieces.forEach(p => {{
      p.y += p.speed;
      p.rotation += 2;
      if (p.y > canvas.height) {{
        p.y = -p.size;
        p.x = Math.random() * canvas.width;
      }}
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rotation * Math.PI / 180);
      ctx.fillStyle = p.color;
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
      ctx.restore();
    }});
    animationId = requestAnimationFrame(update);
  }}

  update();

  // Stop the animation after 3 seconds
  setTimeout(() => {{
    cancelAnimationFrame(animationId);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }}, 3000);
}})();
</script>
<canvas id="fireworks-canvas" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:1000;pointer-events:none;"></canvas>
<script>
(function() {{
  const canvas = document.getElementById("fireworks-canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const fireworks = [];
  function createFirework() {{
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height / 2;
    for (let i = 0; i < 100; i++) {{
      fireworks.push({{
        x, y,
        radius: Math.random() * 2 + 1,
        angle: Math.random() * Math.PI * 2,
        speed: Math.random() * 5 + 2,
        alpha: 1,
        color: `hsl(${{Math.random() * 360}}, 100%, 70%)`
      }});
    }}
  }}

  function updateFireworks() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    fireworks.forEach((p, i) => {{
      const vx = Math.cos(p.angle) * p.speed;
      const vy = Math.sin(p.angle) * p.speed;
      p.x += vx;
      p.y += vy;
      p.alpha -= 0.01;
      if (p.alpha <= 0) fireworks.splice(i, 1);
      else {{
        ctx.globalAlpha = p.alpha;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
      }}
    }});
    ctx.globalAlpha = 1;
    requestAnimationFrame(updateFireworks);
  }}

  for (let i = 0; i < 5; i++) {{
    setTimeout(createFirework, i * 500);
  }}

  updateFireworks();
}})();
</script>

</body>
</html>
        """

  connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "412356",
    database = "secure_vote_db"
  )

  if(connect.is_connected()):
    cursor = connect.cursor()
  
  cursor.execute("SELECT email FROM voters")
  emails = cursor.fetchall()
  print(emails)

  sender = "electora.securevote@gmail.com"
  subject = "Poll Results - "+str(date.today())
  smtp_server = "smtp.gmail.com"
  smtp_port = 587
  password = "jhhe ehco wamv zqax"

  try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
      server.starttls()
      server.login(sender, password)

      for (receiver,) in emails:
        if "example.com" not in receiver:
          msg = MIMEMultipart("alternative")
          msg["From"] = sender
          msg["To"] = receiver
          msg["Subject"] = subject
          
          msg.attach(MIMEText(text, "plain"))
          msg.attach(MIMEText(html, "html"))

          with open('LOGO.png', 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<LOGO>')
            msg.attach(img)

          server.sendmail(sender, receiver, msg.as_string())
      
      messagebox.showinfo("✅","Results have been successfully sent via all Voter's Registered Emails")

      server_host = "MSB"
      server_port = 12345

      client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client_socket.connect((server_host, server_port))
      message = {"poll_status":"ended"}
      client_socket.send(pickle.dumps(message))
      client_socket.close()
      
  except Exception as e:
    messagebox.showerror("Error", e)

def display_live_stats():
  global stats_window, canvas, anext

  stats_window = Toplevel(root)
  stats_window.title("Poll Live Stats")
  stats_window.geometry('1150x764')

  fig, ax = plt.subplots(figsize=(11, 6))
  canvas = FigureCanvasTkAgg(fig, master=stats_window)
  canvas.get_tk_widget().pack(pady=20)

  connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "412356",
    database = "secure_vote_db"
  )

  if(connect.is_connected()):
    cursor = connect.cursor()
  
  cursor.execute("SELECT DISTINCT RIGHT(symbol, 3) from poll_info")
  all_parties = [row[0] for row in cursor.fetchall()]
  
  def refresh_graph():
        ax.clear()

        with open("vote_results.csv", "r") as file:
            reader = csv.reader(file)
            voted_parties = [row[0] for row in reader if row]

        # Count and draw updated stats
        vote_count = Counter(voted_parties) 
        
        votes = [vote_count.get(i, 0) for i in all_parties] 
        
        ax.bar(all_parties, votes, color="skyblue", width = 0.4)
        ax.set_xlabel("Party")
        ax.set_ylabel("Votes")
        ax.set_title("Live Election Vote Stats")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        canvas.draw()
        stats_window.after(2000, refresh_graph)

        if vote_count:
          max_votes = max(vote_count.values())
          winners = [name for name, count in vote_count.items() if count == max_votes]
        else:
          winners = []

        current_time = time.strftime("%H:%M")

        if(current_time < poll_time):
          cursor.close()
          connect.close()
          end_poll_button = Button(stats_window, text = "End Poll", font = ("Tahoma", 15), command = lambda: end_poll(winners))
          end_poll_button.place(x = 1057, y = 0)
        elif(current_time == poll_time):
          messagebox.showinfo("Time Up","The Poll has ended. Sending Results to Voters")
          end_poll(winners)
          stats_window.destroy()
        
  refresh_graph()
    
def send_to_server(poll_data):
  SERVER_HOSTNAME = "MSB"
  SERVER_PORT = 12345
  
  try:
    SERVER_IP = socket.gethostbyname(SERVER_HOSTNAME)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    data = pickle.dumps(poll_data)
    client_socket.sendall(data)
    client_socket.close()
    messagebox.showinfo("Success", "Poll submitted Successfully")
    
    current_time = time.strftime("%H:%M")
    if(current_time < poll_time):
      display_live_stats()
      root.withdraw()
    else:
      messagebox.showinfo("Time Exceeded","The live stats can only be viewed until 5:00pm IST\n\nNote: To retain poll information, please do not shut down or close the server. Doing so will result in the loss of all poll data.")
  except Exception as e:
    messagebox.showerror("Failed", f"Failed to connect to Server: {e}")

def submitpoll():
  for i in names:
    if(i == '' or i.get() == ''):
      messagebox.askretrycancel("Error","Please fill the all the fields to submit poll")
      break

  for i in image_vars:
    if(i == '' or i.get() == ''):
      messagebox.askretrycancel("Error","Please select symbol(s) to submit poll")
      break
  
  name_values = [i.get() for i in names]
  image_values = [i.get() for i in image_vars]
  
  if(len(set(name_values)) != len(name_values)):
    messagebox.askretrycancel("Name Error","Duplicate entries are not allowed. To retry, refresh the page")
    return
  
  if(len(set(image_values)) != len(image_values)):
    messagebox.askretrycancel("Symbol Error","Duplicate entries are not allowed. To retry, refresh the page")
    return

  poll_data = []

  for i in range(len(names)):
    if(names[i].get() == "" or image_vars[i].get() == ""):
      messagebox.askretrycancel("Error", "Please fill all fields to submit poll")
      return

    poll_data.append({"name": names[i].get(), "symbol": image_vars[i].get()})

  agreement = messagebox.askyesno("Terms and Conditions",
        "By using the Electora Secure Vote platform, the poll administrator agrees to adhere strictly to all ethical and legal guidelines governing fair voting practices. The administrator is solely responsible for:\n1. The integrity and security of the polls they create and manage.\n2. Ensuring that no unauthorized or malicious activity (e.g., tampering with votes, voter impersonation, or data misuse) that occurs under their supervision.\nIn the event of any detected or reported malicious activity, including but not limited to vote manipulation, unauthorized access, or violation of user privacy, the poll administrator shall be held fully accountable.\nElectora Secure Vote shall not be liable for any consequences resulting from the misuse of administrative privileges.\n\nClick Yes to accept the Terms and Conditions and proceed"
        )
  if agreement:
    send_to_server(poll_data)
  else:
    messagebox.showinfo("Declined", "You must accept the terms to proceed.")

def reset():
  messagebox.showinfo("Reset","Please wait while the page is reloaded")
  os.startfile("Poll2.py")
  root.destroy()


def display():
  global name_entry, combobox, submit_poll, refresh_button

  n_fetch = int(no_of_candidates.get())

  for i in range(n_fetch):
    Label(root, text = f"{i+1}. Name:", font = ("Tahoma", 11), bg = "white" ).place(x = 275, y = 395 + i * 30) 

    name_var = StringVar()
    name_entry = Entry(root, textvariable = name_var, font = ("Tahoma", 11), width = 25, bg = "white smoke").place(x = 355, y = 395 + i * 30)
    names.append(name_var)
    
    Label(root, text = "Symbol:", font = ("Tahoma", 11), bg = "white").place(x = 575, y = 395 + i * 30)

    image_var = StringVar()
    combobox = ttk.Combobox(root, textvariable = image_var, values = images, state = "readonly", width = 24, font = ("Calibri", 12))
    combobox.place(x = 655, y = 395 + i * 30)
    image_vars.append(image_var)

    y = 395 + i * 30

  submit_poll = Button(root, text = "Submit Poll", font = ("Tahoma", 12), command = submitpoll)
  submit_poll.place(x = 515, y = y + 40)

  reset_button = Button(root, text = " ↻ ", font = ("Calibri", 8), command = reset)
  reset_button.place(x = 868, y = 363)

canvas = Canvas(root, width=1150, height=764)
canvas.pack(fill = "both", expand = True)

image = Image.open("BACKGROUND-Poll2.png")
photo = ImageTk.PhotoImage(image)

canvas.create_image(0, 0, anchor = "nw", image=photo)

Label(root, text = "POLL MAKER", font = ("Tahoma", 16), bg = "white").place(x = 515, y = 300)
Label(root, text = "Enter the following details of the poll", font = ("Tahoma", 10), bg = "white").place(x = 465, y = 330)

Label(root, text = "Select the number of candidates/parties:", font = ("Tahoma", 12), bg = "white").place(x = 270, y = 360)
number = ttk.Combobox(root, width = 27, textvariable = no_of_candidates, font = ("Tahoma", 12))
number['values'] = ('2', '3', '4', '5', '6', '7')
number.place(x = 570, y = 363)
number.current()

select_button = Button(root, text = "✅", font = ("Calibri", 8), command = display).place(x = 840, y = 363)

symbols = Button(root, text = "Symbols Glossary", font = ("Tahoma", 10), command = display_glossary).place(x = 1037, y = 0)

root.mainloop()