from cryptography.fernet import Fernet

# Your generated key used in the script
key = b'key-that-you-have-generated-in-key.key-file' #paste your key here
cipher_suite = Fernet(key)

# Encrypted log data 
encrypted_log = b'log.txt-file-content-paste-here' # paste log.txt file here

def decrypt_message(encrypted_message):
    return cipher_suite.decrypt(encrypted_message).decode()

# Decrypt the log data
decrypted_log = decrypt_message(encrypted_log)
print(decrypted_log)
