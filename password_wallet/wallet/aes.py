from Crypto.Cipher import AES
import os

def encrypt_AES_GCM(password):
    x = os.getenv("SECRET_KEY_PASS")
    aes_cipher = AES.new(x.encode("utf-8"), AES.MODE_GCM)
    ciphertext, auth_tag = aes_cipher.encrypt_and_digest(password.encode("utf-8"))
    return ciphertext, aes_cipher.nonce, auth_tag

def decrypt_AES_GCM(encrypted_msg):
    (ciphertext, nonce, auth_tag) = encrypted_msg
    aes_cipher = AES.new(bytes(os.getenv("SECRET_KEY_PASS")), AES.MODE_GCM, nonce)
    plaintext = aes_cipher.decrypt_and_verify(ciphertext, auth_tag)
    return plaintext