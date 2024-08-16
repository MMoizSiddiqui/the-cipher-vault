import random
import string
import time
import getpass
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

with open("private.pem", "rb") as privatefile:
    privatekey = RSA.import_key(privatefile.read())

with open("public.pem", "rb") as publicfile:
    publickey = RSA.import_key(publicfile.read())

# Cipher objects
RSAencoder = PKCS1_OAEP.new(publickey)
RSAdecoder = PKCS1_OAEP.new(privatekey)

def encrypt(words):
    words = words.split(" ")
    encryptedWords = []

    for word in words:
        randchr1 = ''.join(random.choices(string.ascii_lowercase, k=3))
        randchr2 = ''.join(random.choices(string.ascii_uppercase, k=3))

        if len(word) >= 3:
            st = word[1:] + word[0]
            st = randchr1 + st + randchr2
            
            # Encrypting using RSA algo
            encryptedst = RSAencoder.encrypt(st.encode('utf-8'))
            encryptedWords.append(encryptedst.hex())
        elif len(word) == 2:
            # Caesar cipher encryption
            encryptedword = ""
            for character in word:
                newchar = chr((ord(character) + 3) % 256)
                encryptedword += newchar
            encryptedWords.append(encryptedword) 
        else:
            encryptedWords.append(word)

    return " ".join(encryptedWords)


def decrypt(words):
    words = words.split(" ")
    decryptedWords = []

    for word in words:
        if len(word) >= 6:
            try:
                # Decrypting using RSA algo
                encryptedst = bytes.fromhex(word)
                st = RSAdecoder.decrypt(encryptedst).decode('utf-8')

                st = st[3:-3]
                st = st[-1] + st[:-1]
                decryptedWords.append(st)
            except Exception as e:
                print(f"Decryption error for {word}: {e}")
                decryptedWords.append("[FORMATERROR]")       
        elif len(word) == 2:
            # Caesar cipher decryption
            decryptedword = ""
            for character in word:
                newchar = chr((ord(character) - 3) % 256)
                decryptedword += newchar
            decryptedWords.append(decryptedword)
        else:
            decryptedWords.append(word)

    return " ".join(decryptedWords)


def printPublicKey():
    print("\n--- Public Key ---")
    print(publickey.decode('utf-8'))

def authentication():
    correctPin = "1234"
    overrideKey = "unlock123"
    maxAttempts = 3
    attempts = 0

    while attempts < maxAttempts:
        print("\n⚠️ 🔑 🔑 🔑 🔑 🔑 🔑 ⚠️")
        pin = getpass.getpass("Enter your PIN to unlock : ")

        if pin == correctPin:
            print("Access granted. PIN is correct.")
            return True
        else:
            print("Incorrect PIN. Try again.")
            attempts += 1

        if attempts == maxAttempts:
            print("\n!!! MAX ATTEMPTS REACHED !!!")
            print("Program is temporarily locked for 50 seconds.")
            time.sleep(3)
            print("\nReady to try again.")
            key = input("\nEnter the BYPASS key to unlock: ")

            if key == overrideKey:
                print("BYPASS key accepted. Access granted.")
                return True
            else:
                print("Invalid BYPASS key. Exiting program.")
                sys.exit()

def interface():
    char = "*"
    char2 = "🚫"
    title = "THE CIPHER VAULT"
    subheading = "ENCODING & DECODING PROGRAM"
    status = "SECURITY MODULE ACTIVE"
    warning = "UNAUTHORIZED ACCESS IS PROHIBITED!"
    
    print("\n" + char * (44 + 3 * 2))
    print(f"{char2 * 3} {title.center(36)} {char2 * 3}")
    print(char * (44 + 3 * 2))
    print(f"{char2 * 3} {subheading.center(36)} {char2 * 3}")
    print(char * (44 + 3 * 2))
    print(f"{char2 * 3} {status.center(36)} {char2 * 3}")
    print(char * (44 + 3 * 2))
    print(f"{char2 * 3} {warning.center(36)} {char2 * 3}")
    print(char * (44 + 3 * 2))

def mainMenu():
    interface()
    
    while True:
        print("\nPlease select an option:")
        print("1. Encrypt")
        print("2. Decrypt")
        print("0. Exit")
        choice = input("\nEnter your choice: ")
        if choice == '1':
            words = input("\nEnter a string to be encrypted: ")
            encryptedMessage = encrypt(words)
            print("\nENCRYPTED MESSAGE !!!!! :\n")
            print(encryptedMessage)
        
        elif choice == '2':
            attempts = 0
            while attempts < 3:
                start = time.time()
                print("\nSESSION EXPIRES IN 6 SECONDS. BE CAREFUL!")
                words = input("\n\nEnter a string to be decrypted: ")
                if time.time() - start <= 6:
                    decryptedMessage = decrypt(words)
                    if "[FORMATERROR]" in decryptedMessage:
                        attempts += 1
                        print(f"\nAttempts remaining: {3 - attempts}")
                        print("\n<<<<< INVALID INPUT >>>>>")
                    else:
                        print("\nDECRYPTED MESSAGE !!!!! :\n")
                        print(decryptedMessage)
                        break
                else:
                    print("\nTime's up! Try again.")
                    attempts += 1
                    print(f"\nAttempts remaining: {3 - attempts}")

                if attempts == 3:
                    print("\nYou've exhausted all attempts.")
                    sys.exit()
        elif choice == '0':
            print("\nExiting program...")
            print()
            sys.exit()
        else:
            print("\nInvalid choice. Please enter 1 to encode, 2 to decrypt, or 0 to exit.")
#printPublicKey()
print("\n\n")
print(" "*10 + "🔐 SECURE ACCESS PORTAL 🔐" + " "*10)
if authentication():
    mainMenu()
