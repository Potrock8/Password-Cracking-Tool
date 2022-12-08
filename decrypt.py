import cryptography
from cryptography.fernet import Fernet
import json
"""
Given a filename (str) and key (bytes), it decrypts the file and write it
"""
filename = input("File name: ")
keypath = input("Key: ")
f = open(filename)
data = json.load(f)
filename = data['New generated zip password(encrypted):']
with open(keypath, "rb") as key_file:
    key = key_file.read()

f = Fernet(key)

# decrypt data
decrypted_data = f.decrypt(filename)
# write the original file
print(decrypted_data.decode())