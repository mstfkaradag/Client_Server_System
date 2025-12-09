from .base import Cipher
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class AesLib(Cipher):
    def __init__(self, key):
        self.key = key.encode('utf-8')
        if len(self.key) < 16:
            self.key = self.key.ljust(16, b'0')
        elif len(self.key) > 16:
            self.key = self.key[:16]

    def encrypt(self, text):
        try:
            cipher = AES.new(self.key, AES.MODE_CBC)

            ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))

            return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
        except Exception as e:
            return f"AES Şifreleme Hatası: {str(e)}"
        
    def decrypt(self, text):
        try:
            raw = base64.b64decode(text)

            iv = raw[:16]
            ct = raw[16:]

            cipher = AES.new(self.key, AES.MODE_CBC, iv)

            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except Exception as e:
            return f"AES Deşifreleme Hatası: {str(e)}"