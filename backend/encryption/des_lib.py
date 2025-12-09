from .base import Cipher
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

class DesLib(Cipher):
    def __init__(self, key):
        self.key = key.encode('utf-8')
        if len(self.key) < 8:
            self.key = self.key.ljust(8, b'0')
        elif len(self.key) > 8:
            self.key = self.key[:8]

    def encrypt(self, text):
        try:
            cipher = DES.new(self.key, DES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), DES.block_size))
            return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
        except Exception as e:
            return f"DES Şifreleme hatası: {str(e)}"
        
    def decrypt(self, text):
        try:
            raw = base64.b64decode(text)
            iv = raw[:8]
            ct = raw[8:]

            cipher = DES.new(self.key, DES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), DES.block_size)
            return pt.decode('utf-8')
        except Exception as e:
            return f"DES Deşifreleme hatası: {str(e)}"