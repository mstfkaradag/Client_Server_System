from .base import Cipher

class VigenereCipher(Cipher):

    def __init__(self, key):
        if not isinstance(key, str) or key.strip() == "":
            raise ValueError("Key boş olamaz.")
        self.key = key

    def _key_shifts(self, key):
        upper_a_ascii = ord('A')
        index = []

        for ch in key:
            if ch.isalpha():
                i = ord(ch.upper()) - upper_a_ascii
                index.append(i)
        return index

    def encrypt(self, text):
        if not isinstance(text, str) or text.strip() == "":
            raise TypeError("Text bir string olmalıdır")
        k_shifts = self._key_shifts(self.key)
        if not k_shifts:
            raise ValueError("Key alfabetik olmalıdır")
        
        out = []
        k_i = 0
        k_len = len(k_shifts)
        for ch in text:
            if 'A' <= ch <= 'Z':
                shift = k_shifts[k_i % k_len]
                out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
                k_i += 1
            elif 'a' <= ch <= 'z':
                shift = k_shifts[k_i % k_len]
                out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
                k_i += 1
            else:
                out.append(ch)
        return ''.join(out)

    def decrypt(self, text):
        if not isinstance(text, str) or text.strip() == "":
            raise TypeError("Text bir string olmalıdır")
        k_shifts = self._key_shifts(self.key)
        if not k_shifts:
            raise ValueError("Key alfabetik olmalıdır")
        
        out = []
        k_i = 0
        k_len = len(k_shifts)
        for ch in text:
            if 'A' <= ch <= 'Z':
                shift = k_shifts[k_i % k_len]
                out.append(chr((ord(ch) - 65 - shift) % 26 + 65))
                k_i += 1
            elif 'a' <= ch <= 'z':
                shift = k_shifts[k_i % k_len]
                out.append(chr((ord(ch) - 97 - shift) % 26 + 97))
                k_i += 1
            else:
                out.append(ch)
        return ''.join(out)