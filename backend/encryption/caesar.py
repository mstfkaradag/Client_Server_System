from .base import Cipher
from typing import Union

class CaesarCipher(Cipher):

    def __init__(self, shift: Union[int, str]):
        try:
            s = int(shift)
        except Exception:
            raise ValueError("Anahtar bir tam sayı olmalı veya tam sayıya çevrilebilir bir string olmalıdır.")
        self.shift = s % 26

    @staticmethod
    def _is_ascii_upper(ch) -> bool:
        return 'A' <= ch <= 'Z'
    
    @staticmethod
    def _is_ascii_lower(ch) -> bool:
        return 'a' <= ch <= 'z'

    def _transform(self, text, shift):
        if text is None:
            raise ValueError("Text boş olamaz")
        shift = shift % 26
        out_chars = []
        for char in text:
            if self._is_ascii_upper(char):
                base = ord('A')
                out_chars.append(chr((ord(char) - base + shift) % 26 + base))
            elif self._is_ascii_lower(char):
                base = ord('a')
                out_chars.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                out_chars.append(char)
            
        return ''.join(out_chars)

    def encrypt(self, text):
        return self._transform(text, self.shift)

    def decrypt(self, text):
        return self._transform(text, -self.shift)