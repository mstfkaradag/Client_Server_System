from .base import Cipher

class SubstitutionCipher(Cipher):
    def __init__(self, upper_cipher_alphabet, lower_cipher_alphabet):
        if len(upper_cipher_alphabet) != 26 or len(lower_cipher_alphabet) != 26:
            raise ValueError("Alfabeler 26 karakterli olmalıdır")
        
        self.lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.lower_cipher_alphabet = lower_cipher_alphabet # XNYAHPOGZQWBTSFLRCVMUEKJDI
        self.upper_cipher_alphabet = upper_cipher_alphabet # dlryvohezxwptbgfjqnmuskaci

        self.encrypt_map = {}
        self.decrypt_map = {}

        for la, lca in zip(self.lower_alphabet, self.lower_cipher_alphabet):
            self.encrypt_map[la] = lca
            self.decrypt_map[lca] = la
        for ua, uca in zip(self.upper_alphabet, self.upper_cipher_alphabet):
            self.encrypt_map[ua] = uca
            self.decrypt_map[uca] = ua

    def encrypt(self, text):
        result = []
        for char in text:
            result.append(self.encrypt_map.get(char, char))
        return "".join(result)
    
    def decrypt(self, text):
        result = []
        for char in text:
            result.append(self.decrypt_map.get(char, char))
        return "".join(result)