import os
import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .base import Cipher

class EccLib(Cipher):
    def __init__(self):
        pass

    @staticmethod
    def generate_keys():
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()

        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return pem_private.decode('utf-8'), pem_public.decode('utf-8')

    @staticmethod
    def encrypt(message, public_key_pem):
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')

            peer_public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))

            ephemeral_private_key = ec.generate_private_key(ec.SECP256R1())
            
            shared_key = ephemeral_private_key.exchange(ec.ECDH(), peer_public_key)

            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'handshake data',
            ).derive(shared_key)

            aesgcm = AESGCM(derived_key)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, message, None)

            ephemeral_public_key_bytes = ephemeral_private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            combined = base64.b64encode(ephemeral_public_key_bytes).decode('utf-8') + ":::" + \
                       base64.b64encode(nonce).decode('utf-8') + ":::" + \
                       base64.b64encode(ciphertext).decode('utf-8')
            
            return combined

        except Exception as e:
            raise ValueError(f"ECC Şifreleme Hatası: {str(e)}")

    @staticmethod
    def decrypt(encrypted_package, private_key_pem):
        try:
            parts = encrypted_package.split(":::")
            if len(parts) != 3:
                raise ValueError("Geçersiz ECC şifreli veri formatı")

            pem_ephemeral_public = base64.b64decode(parts[0])
            nonce = base64.b64decode(parts[1])
            ciphertext = base64.b64decode(parts[2])

            my_private_key = serialization.load_pem_private_key(private_key_pem.encode('utf-8'), password=None)

            peer_ephemeral_public_key = serialization.load_pem_public_key(pem_ephemeral_public)

            shared_key = my_private_key.exchange(ec.ECDH(), peer_ephemeral_public_key)

            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'handshake data',
            ).derive(shared_key)

            aesgcm = AESGCM(derived_key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)

            return plaintext.decode('utf-8')

        except Exception as e:
            raise ValueError(f"ECC Deşifreleme Hatası: {str(e)}")