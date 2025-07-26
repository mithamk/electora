 ELECTORA – Secure Voting System

**ELECTORA** is a secure, TCP-based voting system built with strong authentication, real-time visual feedback, and multi-role support. Developed as a 2nd-year Computer Networks project, it provides end-to-end encryption, email and SMS notifications, and dynamic graphical result analysis.

---

## 🔐 Key Features

- Secure communication using `ssl.wrap_socket`
- Admin panel to create and manage polls
- Voter interface with OTP-based authentication
- GUI (Tkinter) and HTML-styled result page
- Real-time graphical result visualization (bar graphs)
- Result auto-emailed to all voters after voting
- SMS alerts using Twilio API
- MySQL database for storing users and votes
- SMTP email service for verification & notifications

---

## ⚙️ How to Run ELECTORA

### Prerequisites

- Python 3.7+
- MySQL installed
- Twilio account (SID, Auth Token, Number)
- SMTP email (Gmail + App Password recommended)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ELECTORA.git
cd ELECTORA

# 2. Install required libraries
pip install -r requirements.txt

# 3. Configure:
# - db_config.py (MySQL credentials)
# - twilio_config.py (SID, Auth Token, Phone)
# - mail_config.py (Email & App password)

# 4. Start the secure server
python secure_server.py

# 5. Run the admin interface to create the poll
python admin_gui.py

# 6. Run the voter interface for each user
python voter_gui.py
