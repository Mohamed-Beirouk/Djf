import base64, rsa, os, hashlib
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Djf.settings import PublicKEYAES




def OnlyOneTime(str):
    (public_key, private_key) = rsa.newkeys(2048)
    private_key_pem = private_key.save_pkcs1()
    with open('private_key_django.pem', 'wb') as f:
        f.write(private_key_pem)
    public_key_pem = public_key.save_pkcs1()
    with open('public_key_django.pem', 'wb') as f:
        f.write(public_key_pem)

OnlyOneTime("yalla")

    
def encryptRSA(message):
    with open('public_key_django.pem', 'rb') as f:
        public_key_pem = f.read()
        public_key = rsa.PublicKey.load_pkcs1(public_key_pem)

    # Encrypt the message using the public key
    ciphertext = rsa.encrypt(message.encode(), public_key)

    # Encode the ciphertext to base64
    ciphertext_base64 = base64.b64encode(ciphertext)
    
    # Return the base64 encoded ciphertext as string
    return ciphertext_base64
    
def decryptRSA(encrypted_message):
    # Load private key from PEM file
    with open('private_key_django.pem', 'rb') as f:
        private_key_pem = f.read()
        private_key = rsa.PrivateKey.load_pkcs1(private_key_pem)

    message = base64.b64decode(encrypted_message)

    enc = rsa.decrypt(message, private_key)

    return str(enc)[2:-1]


# def encrypt_decrypt_data(data, key, data_type, mode):
    
#     if mode == 'encrypt':
#         if data_type == 'string':
#             cipher = AES.new(key, AES.MODE_EAX)
#             ciphertext, tag = cipher.encrypt_and_digest(data)
#             return ciphertext, tag
#     elif mode == 'decrypt':
#         if data_type == 'string':
#             cipher = AES.new(key, AES.MODE_EAX, nonce)
#             data = cipher.decrypt_and_verify(ciphertext, tag)
#         elif data_type == 'file':
#             with open(data, 'rb') as encrypted_file:
#                 data = encrypted_file.read()
#             data = base64.b64decode(data)
#             obj = AES.new(key, AES.MODE_CBC)
#             decrypted_data = obj.decrypt(data)
        
#             with open(data[:-4], 'wb') as file:
#                 file.write(decrypted_data)
#             return decrypted_data
#     else:
#         return None


# def encryptAES(data, data_type='string'):
#     backend = default_backend()
#     key = os.urandom(32)
#     backend = default_backend()
#     cipher = Cipher(algorithms.AES(key), modes.GCM(b'\0' * 12), backend=backend)
#     encryptor = cipher.encryptor()

#     if data_type == 'string':
#         encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
#         tag = encryptor.tag
#         return encrypted_data, key, tag
#     elif data_type == 'file':
#         encrypted_data = data + '.encrypted'
#         with open(data, 'rb') as in_file:
#             with open(encrypted_data, 'wb') as out_file:
#                 while True:
#                     chunk = in_file.read(4096)
#                     if len(chunk) == 0:
#                         break
#                     out_file.write(encryptor.update(chunk))
#                 out_file.write(encryptor.finalize())
#         tag = encryptor.tag
#         return encrypted_data, key, tag
#     else:
#         raise ValueError('Invalid data_type argument. Must be "string" or "file".')

# def decryptAES(encrypted_data, key, tag, data_type='string'):
#     backend = default_backend()
#     cipher = Cipher(algorithms.AES(key), modes.GCM(b'\0' * 12, tag), backend=backend)
#     decryptor = cipher.decryptor()

#     if data_type == 'string':
#         decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
#         return decrypted_data.decode()
#     elif data_type == 'file':
#         decrypted_file = encrypted_data.replace('.encrypted', '')
#         with open(encrypted_data, 'rb') as in_file:
#             with open(decrypted_file, 'wb') as out_file:
#                 while True:
#                     chunk = in_file.read(4096)
#                     if len(chunk) == 0:
#                         break
#                     out_file.write(decryptor.update(chunk))
#                 out_file.write(decryptor.finalize())
#         return decrypted_file
#     else:
#         raise ValueError('Invalid data_type argument. Must be "string" or "file".')



# x="mohamed beirouk"

# print(x)


# print("encrypting .....")
# print(encrypt_message(x))

# print("decrypting .....")
# print(decrypt_message(encrypt_message(x)))



# message = "Mohamed Beirouk"
# print("My original str : "+message)

# enc = encrypt_message(message)

# my_str = str(enc)
# print("Encrypted message : "+my_str)


# my_str_as_bytes = str.encode(my_str)
# encr = decrypt_message(my_str_as_bytes)

# print("decrypted str: "+encr)



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



def encryptAES(plaintext, key):
    byteKEY = base64.b64decode(key)
    cipher = AES.new(byteKEY, AES.MODE_ECB)
    # padded_plaintext = Padding.pad(plaintext, AES.block_size, style='pkcs7')
    encrypted_data = cipher.encrypt(pad(plaintext.encode("utf8"), 16))
    return base64.b64encode(encrypted_data).decode("utf-8")


def decryptAES(encrypted_data, key):
    
    # Create a cipher object and decrypt the encrypted data
    byteKEY = base64.b64decode(key) 
    encrypted_data = base64.b64decode(encrypted_data)
    cipher = AES.new(byteKEY, AES.MODE_ECB)
    plaintext = cipher.decrypt(encrypted_data)
    # plaintext = Padding.unpad(padded_plaintext, AES.block_size, style='pkcs7')
    return unpad(plaintext, 16)


