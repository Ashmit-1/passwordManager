import rsa

def generate_keys():
    public_key, private_key = rsa.newkeys(256)
    with open ("private_key.pem", 'wb') as keys:
        keys.write(private_key.save_pkcs1('PEM'))

    with open ("public_key.pem", 'wb') as keys:
        keys.write(public_key.save_pkcs1('PEM'))

def encryption(message):
    with open ("public_key.pem", 'rb') as keys:
        public_key = rsa.PublicKey.load_pkcs1(keys.read())
    encrypted_message = rsa.encrypt(message.encode(), public_key)
    return encrypted_message

def decryption(message):
    with open ("private_key.pem", 'rb') as keys:
        private_key = rsa.PrivateKey.load_pkcs1(keys.read())
    decrypted_message = rsa.decrypt(message, private_key)
    return decrypted_message.decode()


