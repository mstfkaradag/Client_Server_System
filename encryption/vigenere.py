class VigenereCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, text, key = None):
        if key is None:
            key = self.key
        result = ""
        pattern = (key * ((len(text) // len(key)) + 1))[:len(text)]
        for i, char in enumerate(text):
            if char.isupper():
                result = result + chr((ord(char) - 65 + (ord(pattern[i].upper()) - 65)) % 26 + 65)
            elif char.islower():
                result = result + chr((ord(char) - 97 + (ord(pattern[i].lower()) - 97)) % 26 + 97)
            else:
                result = result + char

        return result

    def decrypt(self, text, key = None):
        if key is None:
            key = self.key
        result = ""
        pattern = (key * ((len(text) // len(key)) + 1))[:len(text)]
        for i, char in enumerate(text):
            if char.isupper():
                result = result + chr((ord(char) - 65 - (ord(pattern[i].upper()) - 65)) % 26 + 65)
            elif char.islower():
                result = result + chr((ord(char) - 97 - (ord(pattern[i].lower()) - 97)) % 26 + 97)
            else:
                result = result + char

        return result