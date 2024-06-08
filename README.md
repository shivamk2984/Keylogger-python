# Python Keylogger with Email Reporting

## Description

This project is a Python-based keylogger that captures keystrokes and periodically emails the encrypted logs to a specified email address. The logs are encrypted using the `cryptography` library, ensuring the captured data remains secure.

## Features

- Captures keystrokes and logs them to a file.
- Encrypts the log file using `Fernet` symmetric encryption.
- Periodically emails the encrypted log file to a specified email address.
- Runs as a background process on Windows systems.
- Uses Gmail's SMTP server for sending emails.

## Prerequisites

- Python 3.x
- A Gmail account (with app-specific password if using 2FA)

## How to decrypt
once you recieve log.txt file on you email, copy the contents of it and paste it into decrypt_log.py
