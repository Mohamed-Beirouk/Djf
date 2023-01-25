import rsa
import pickle


(pubkey, privkey) = rsa.newkeys(512)

with open("private.pem", "wb") as f:
    f.write(pickle.dumps(privkey))

with open("public.pem", "wb") as f:
    f.write(pickle.dumps(pubkey))

# Load keys from file
with open("private.pem", "rb") as f:
    private_key = pickle.loads(f.read())

with open("public.pem", "rb") as f:
    public_key = pickle.loads(f.read())

# Encryption function
def encrypt_message(message, public_key):
    return rsa.encrypt(message.encode(), public_key)

# Decryption function
def decrypt_message(encrypted_message, private_key):
    return rsa.decrypt(encrypted_message, private_key).decode()

# Test encryption and decryption
message = "This is a test message"
encrypted_message = encrypt_message(message, public_key)
print(encrypted_message)
print(decrypt_message(encrypted_message, private_key))