from .base import Cipher

class PigpenCipher(Cipher):
    def __init__(self):
        pass

    def encrypt(self, text):
        if not text: return ""
        text = text.lower()
        result = []
        
        for char in text:
            if 'a' <= char <= 'z':
                result.append(f"{char}.png")
            elif char == ' ':
                result.append("space")
            else:
                result.append(char)
        
        return ",".join(result)

    def decrypt(self, text):
        if not text: return ""
        
        parts = text.split(',')
        result = ""
        
        for part in parts:
            if part.endswith(".png"):
                result += part[0].upper()
            elif part == "space":
                result += " "
            else:
                result += part
                
        return result