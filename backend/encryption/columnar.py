from .base import Cipher
import math

class ColumnarTransposition(Cipher):
    def __init__(self, key):
        if not key or not isinstance(key, str):
            raise ValueError("Anahtar bir kelime olmalıdır (Örn: TRUVA).")
        self.key = key.upper().replace(" ", "")
        
    def _get_column_order(self):
        key_indexed = [(ch, i) for i, ch in enumerate(self.key)]
        key_sorted = sorted(key_indexed, key=lambda x: x[0])
        return [item[1] for item in key_sorted]

    def encrypt(self, text):
        if not text: return ""
        text = text.upper().replace(" ", "")
        
        num_cols = len(self.key)
        num_rows = math.ceil(len(text) / num_cols)
        
        missing_chars = (num_rows * num_cols) - len(text)
        text += '*' * missing_chars
        
        grid = []
        for i in range(num_rows):
            start = i * num_cols
            end = start + num_cols
            grid.append(list(text[start:end]))
            
        col_order = self._get_column_order()
        result = []
        
        for col_index in col_order:
            for row in range(num_rows):
                result.append(grid[row][col_index])
                
        return "".join(result)

    def decrypt(self, text):
        if not text: return ""
        
        num_cols = len(self.key)
        num_rows = math.ceil(len(text) / num_cols)
        col_order = self._get_column_order()
        
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        
        current_idx = 0
        for col_index in col_order:
            for row in range(num_rows):
                if current_idx < len(text):
                    grid[row][col_index] = text[current_idx]
                    current_idx += 1
                    
        result = []
        for row in range(num_rows):
            for col in range(num_cols):
                result.append(grid[row][col])
        
        return "".join(result).rstrip('*')