import rsa
import pickle

# def oneTimeInDenye(self):
#     (pubkey, privkey) = rsa.newkeys(512)

#     with open("private.pem", "wb") as f:
#         f.write(pickle.dumps(privkey))

#     with open("public.pem", "wb") as f:
#         f.write(pickle.dumps(pubkey))


def encrypt_message(message):
    with open("public.pem", "rb") as f:
        public_key = pickle.loads(f.read())
    return rsa.encrypt(message.encode(), public_key)

def decrypt_message(encrypted_message):
    with open("private.pem", "rb") as f:
        private_key = pickle.loads(f.read())
    return rsa.decrypt(encrypted_message, private_key).decode()

message = "This is a test message"
encrypted_message = encrypt_message(message)
print(encrypted_message)
print(decrypt_message(encrypted_message))


# def get_public_key(self):
#     with open('keys/publcKey.pem', 'rb') as p:
#         publicKey = rsa.PublicKey.load_pkcs1(p.read())
#         return publicKey

# def get_private_key(self):
#     with open('keys/privateKey.pem', 'rb') as p:
#         privateKey = rsa.PrivateKey.load_pkcs1(p.read())
#         return privateKey



# def encrypt(self,message):

#     # read the PEM file containing the RSA public key
#     with open("public_key.pem", "rb") as key_file:
#         public_key = RSA.import_key(key_file.read())
#     cipher = PKCS1_OAEP.new(public_key)
#     encrypted_message = cipher.encrypt(message.encode())
#     return encrypted_message


# def decrypt(ciphertext):
#     try:
#         return rsa.decrypt(ciphertext, get_private_key).decode()
#     except:
#         return False
    


# def sign(message, key):
#     return rsa.sign(message.encode('ascii'), key, 'SHA-1')


# def verify(message, signature, key):
#     try:
#         return rsa.verify(message.encode('ascii'), signature, key,) == 'SHA-1'
#     except:
#         return False