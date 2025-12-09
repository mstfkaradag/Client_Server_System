from .base import Cipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class RsaLib(Cipher):
    def __init__(self, key = None, is_private = False):
        self.key = key
        self.is_private = is_private
        self.cipher_rsa = None

        if self.key:
            try:
                self.rsa_key = RSA.import_key(self.key)
                self.cipher_rsa = PKCS1_OAEP.new(self.rsa_key)
            except Exception as e:
                pass
        
    def encrypt(self, text):
        if not self.cipher_rsa:
            return "Hata: RSA Public Key yüklenemedi."
        try:
            enc_data = self.cipher_rsa.encrypt(text.encode('utf-8'))
            return base64.b64encode(enc_data).decode('utf-8')
        except Exception as e:
            return f"RSA Şifreleme hatası: {str(e)}"
        
    def decrypt(self, text):
        if not self.cipher_rsa or not self.is_private:
            return "Hata: RSA Private Key gerekli"
        try:
            raw_cipher = base64.b64decode(text)
            decrypted_text = self.cipher_rsa.decrypt(raw_cipher)
            return decrypted_text.decode('utf-8')
        except Exception as e:
            return f"RSA Deşifreleme hatası: {str(e)}"
        
    @staticmethod
    def generate_keys():
        key = RSA.generate(2048)
        private_key = key.export_key().decode('utf-8')
        public_key = key.public_key().export_key().decode('utf-8')
        return private_key, public_key