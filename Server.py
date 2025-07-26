import socket
import pickle
import mysql.connector
import smtplib
import random
import threading
from twilio.rest import Client
import time
import csv

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 12345

connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "412356",
    database = "secure_vote_db",
    charset = 'utf8mb4',
    collation = 'utf8mb4_unicode_ci'
)

if(connect.is_connected()):
    cursor = connect.cursor()

data = []
current_time = time.strftime("%H:%M")
poll_end_time = "17:00"

if(current_time < poll_end_time):
    poll_open = True
else:
    poll_open = False

print(poll_open)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listenting on port {SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        client_thread = threading.Thread(target = handle_client, args = (client_socket,))
        client_thread.start()

def store_vote(voter_id, vote_data):
    with open("vote_results.csv", "a", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow([vote_data['symbol'][-3:]])
    
    query = "UPDATE voters SET voted = 1 WHERE voter_id = %s"
    values = (voter_id,)
    cursor.execute(query, values)
    connect.commit()

def handle_client(client_socket):
    global poll_open
    try:
        data = client_socket.recv(4096)
        request_data = pickle.loads(data)

        print(request_data)
        print(poll_open)

        if "check_voter" in request_data:
            voter_data = request_data["check_voter"]
            flag = check_voter(voter_data)
            client_socket.send(pickle.dumps(flag))
        if "authenticated" in request_data:
            if request_data['authenticated'] is True:
                client_socket.send(pickle.dumps({"status": "success", "poll_info": get_poll_info()}))
            else:
                client_socket.send(pickle.dumps({"status": "auth_failed"}))
        elif "voter_id" in request_data and "vote" in request_data:
            if(poll_open == True):
                store_vote(request_data["voter_id"], request_data["vote"])
                print(f"Vote from {request_data['voter_id']} for {request_data['vote']['symbol']} stored successfully.")
                client_socket.send(pickle.dumps({"status": "vote_received"}))
            else:
                client_socket.send(pickle.dumps({"status":"ended"}))
        elif "poll_status" in request_data and request_data["poll_status"] == "ended":
            poll_open = False
            print("Poll Open Status:", poll_open, "\nPoll Status Ended")
        else:
            save_poll_data(request_data)
            print("Poll received Successfully")        
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

def get_poll_info():
    if(poll_open == False):
        return -1
    
    global data 
    return data

def save_poll_data(poll_data):
    for i in poll_data:
        query = """
        INSERT INTO poll_info (candidate_name, symbol)
        VALUES (%s, %s)
        """
        values = (i['name'], i['symbol']) 
        cursor.execute(query, values)
        data.append({"name": i['name'], "symbol": i['symbol']})

    connect.commit()

def generate_otp():
    return str(random.randint(1000, 9999))

def check_voter(voter_data):
    if(poll_open == False):
        return -2
    
    with connect.cursor() as cursor:
        query = """
        SELECT COUNT(*) FROM voters where voter_id = %s AND email = %s AND phone_number = %s
        """
        values = (voter_data['voter_id'], voter_data['email'], voter_data['phone_number'])
        cursor.execute(query, values)

        result = cursor.fetchone()

        if(result[0] == 1): #voter found
            query = "SELECT voted from voters where voter_id = %s"
            values = (voter_data['voter_id'],)
            cursor.execute(query, values)
            voted_status = cursor.fetchone()[0]

            if(voted_status == 1):
                return 1 #indicating the voter has voted
            
            query = """
                SELECT voter_id, name, aadhar_number, pan_card, phone_number, email FROM voters where voter_id = %s
            """
            values = (voter_data['voter_id'],)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if(result is not None):
                global otp1, otp2
            
                recipient_email = voter_data['email']
                otp1 = generate_otp()

                sender_email = "electora.securevote@gmail.com"
                sender_password = "jhhe ehco wamv zqax"

                account_sid = 'AC4a6a0830a7b4badaa96f8d019dd6ff75'
                auth_token = '3e4eecb0fc3330f60d945ec7a7fedea7'
                twilio_phone_number = '+16203495737'

                otp2 = generate_otp()

                client = Client(account_sid, auth_token)

                otps = []

                otps.append(otp1)
                otps.append(otp2)

                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, sender_password)

                    subject = "Electora Secure Vote OTP"
                    body = f"Your OTP is {otp1}"
                    message = f"Subject: {subject}\n\n{body}"

                    server.sendmail(sender_email, recipient_email, message)
                    server.quit()
                    
                    sms_message = client.messages.create(
                        body = f"Electora Secure Vote OTP is {otp2}",
                        from_ = twilio_phone_number,
                        to = "+91"+voter_data['phone_number'].strip()
                    )

                    return otps
                except Exception as e:
                    return -1 
            else:
                    return -1
        else:
            return 0

if __name__ == "__main__":
    cursor.execute("TRUNCATE table poll_info")
    cursor.execute("UPDATE voters SET voted = 0")
    open("vote_results.csv", "w").close() 
    connect.commit()
    start_server()