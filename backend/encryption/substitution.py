from .base import Cipher

class SubstitutionCipher(Cipher):
    def __init__(self, upper_cipher_alphabet, lower_cipher_alphabet):
        self.lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.lower_cipher_alphabet = lower_cipher_alphabet # XNYAHPOGZQWBTSFLRCVMUEKJDI
        self.upper_cipher_alphabet = upper_cipher_alphabet # dlryvohezxwptbgfjqnmuskaci

    def encrypt(self, text):
        result = ""
        for char in text:
            if char.isupper():
                for i in range(26):
                    if self.upper_alphabet[i] == char:
                        result = result + self.upper_cipher_alphabet[i]
                        break
            elif char.islower():
                for i in range(26):
                    if self.lower_alphabet[i] == char:
                        result = result + self.lower_cipher_alphabet[i]
                        break
            else:
                result = result + char

        return result
    
    def decrypt(self, text):
        result = ""
        for char in text:
            if char.isupper():
                for i in range(26):
                    if self.lower_cipher_alphabet[i] == char:
                        result = result + self.lower_alphabet[i]
                        break
            elif char.islower():
                for i in range(26):
                    if self.upper_cipher_alphabet[i] == char:
                        result = result + self.upper_alphabet[i]
                        break
            else:
                result = result + char

        return result