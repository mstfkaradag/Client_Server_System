from .base import Cipher
from typing import Union
import math

class RouteCipher(Cipher):
    def __init__(self, key: Union[str, int]):
        try:
            s = int(key)
            if s < 2:
                raise ValueError("Sütun sayısı en az 2 olmalıdır.")
        except Exception:
            raise ValueError("Anahtar tam sayı olmalıdır.")
        self.cols = s

    def encrypt(self, text):
        if not text:
            return ""
        text = text.upper().replace(" ", "")
        
        num_rows = math.ceil(len(text) / self.cols)
        total_cells = num_rows * self.cols
        
        text += '*' * (total_cells - len(text))
        
        grid = []
        for i in range(num_rows):
            grid.append(list(text[i*self.cols : (i+1)*self.cols]))
            
        result = []
        top = 0
        bottom = num_rows - 1
        left = 0
        right = self.cols - 1
        
        direction = 0 
        
        while top <= bottom and left <= right:
            if direction == 0:
                for i in range(top, bottom + 1):
                    result.append(grid[i][right])
                right -= 1
                
            elif direction == 1:
                for i in range(right, left - 1, -1):
                    result.append(grid[bottom][i])
                bottom -= 1
                
            elif direction == 2:
                for i in range(bottom, top - 1, -1):
                    result.append(grid[i][left])
                left += 1
                
            elif direction == 3:
                for i in range(left, right + 1):
                    result.append(grid[top][i])
                top += 1
            
            direction = (direction + 1) % 4
            
        return "".join(result)

    def decrypt(self, text):
        if not text: return ""
        
        total_cells = len(text)
        num_rows = math.ceil(total_cells / self.cols)
        
        grid = [['' for _ in range(self.cols)] for _ in range(num_rows)]
        
        top = 0
        bottom = num_rows - 1
        left = 0
        right = self.cols - 1
        direction = 0
        
        idx = 0
        
        while top <= bottom and left <= right and idx < len(text):
            if direction == 0:
                for i in range(top, bottom + 1):
                    grid[i][right] = text[idx]
                    idx += 1
                right -= 1
                
            elif direction == 1:
                for i in range(right, left - 1, -1):
                    grid[bottom][i] = text[idx]
                    idx += 1
                bottom -= 1
                
            elif direction == 2:
                for i in range(bottom, top - 1, -1):
                    grid[i][left] = text[idx]
                    idx += 1
                left += 1
                
            elif direction == 3:
                for i in range(left, right + 1):
                    grid[top][i] = text[idx]
                    idx += 1
                top += 1
            
            direction = (direction + 1) % 4
            
        result = ""
        for row in grid:
            result += "".join(row)
            
        return result.rstrip('*')