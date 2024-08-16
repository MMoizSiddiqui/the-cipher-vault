from Crypto.PublicKey import RSA


key = RSA.generate(2048)


privatekey = key.export_key()
with open("private.pem", "wb") as privatefile:
    privatefile.write(privatekey)


publickey = key.publickey().export_key()
with open("public.pem", "wb") as publicfile:
    publicfile.write(publickey)

print("RSA key pair generated and saved to files.")
