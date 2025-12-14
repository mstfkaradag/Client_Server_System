from .base import Cipher
from typing import Union

class RailFenceCipher(Cipher):
    def __init__(self, key: Union[str, int]):
        try:
            s = int(key)
            if s < 2:
                raise ValueError("Ray sayısı en az 2 olmalıdır.")
        except Exception:
            raise ValueError("Anahtar tam sayı olmalıdır.")
        self.rails = s

    def encrypt(self, text):
        if not text:
            return ""
        text = text.upper().replace(" ", "")
        
        fence = ['' for _ in range(self.rails)]
        
        cycle = 2 * (self.rails - 1)
        
        for i, char in enumerate(text):
            t = i % cycle
            
            if t < self.rails:
                row = t
            else:
                row = cycle - t
            
            fence[row] += char
            
        return "".join(fence)

    def decrypt(self, text):
        if not text: return ""
        text = text.upper().replace(" ", "")
        
        grid = [['' for _ in range(len(text))] for _ in range(self.rails)]
        
        cycle = 2 * (self.rails - 1)
        
        for i in range(len(text)):
            t = i % cycle
            if t < self.rails:
                row = t
            else:
                row = cycle - t
            grid[row][i] = '*'
            
        index = 0
        for r in range(self.rails):
            for c in range(len(text)):
                if grid[r][c] == '*' and index < len(text):
                    grid[r][c] = text[index]
                    index += 1
                    
        result = []
        for i in range(len(text)):
            t = i % cycle
            if t < self.rails:
                row = t
            else:
                row = cycle - t
            result.append(grid[row][i])
            
        return "".join(result)