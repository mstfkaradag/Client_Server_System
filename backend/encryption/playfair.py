from .base import Cipher
import math

class Playfair(Cipher):
    def __init__(self, key):
        self.key = key.upper().replace("J", "I")
        self.alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

        self.matrix = self._create_matrix(self.key)

    def _create_matrix(self, key):
        matrix_string = ""
        seen = set()

        for char in key + self.alphabet:
            if char not in seen and char in self.alphabet:
                matrix_string += char
                seen.add(char)

        result = []
        for i in range(0, 25, 5):
            chunk = matrix_string[i: i + 5]
            row = list(chunk)
            result.append(row)

        return result
    
    def _get_pos(self, char):
        for row in range(5):
            for col in range(5):
                if self.matrix[row][col] == char:
                    return row, col
                
        return None
    
    def _prepare_text(self, text):
        text = text.upper().replace("J", "I").replace(" ", "")
        result = []
        i = 0
        while i < len(text):
            a = text[i]

            if i + 1 >= len(text):
                result.append(a, 'X')
                i += 1
            elif a == text[i + 1]:
                result.append(a, 'X')
                i += 1
            else:
                result.append(a, text[i + 1])
                i += 2
        return result

    def encrypt(self, text):
        pairs = self._prepare_text(text)
        encrypted_text = []
        
        for char1, char2 in pairs:
            row1, col1 = self._get_pos(char1)
            row2, col2 = self._get_pos(char2)

            if row1 == row2:
                col1 = (col1 + 1) % 5
                col2 = (col2 + 1) % 5
            elif col1 == col2:
                row1 = (row1 + 1) % 5
                row2 = (row2 + 1) % 5
            else:
                col1, col2 = col2, col1

            encrypted_text.append(self.matrix[row1][col1] + self.matrix[row2][col2])

        return "".join(encrypted_text)

    def decrypt(self, text):
        text = text.upper().replace(" ", "")
        decrypted_text = []

        for i in range(0, len(text), 2):
            char1 = text[i]
            char2 = text[i + 1] if i + 1 < len(text) else 'X'

            row1, col1 = self._get_pos(char1)
            row2, col2 = self._get_pos(char2)

            if row1 == row2:
                col1 = (col1 - 1) % 5
                col2 = (col2 - 1) % 5
            elif col1 == col2:
                row1 = (row1 - 1) % 5
                row2 = (row2 - 1) % 5
            else:
                col1, col2 = col2, col1
            decrypted_text.append(self.matrix[row1][col1] + self.matrix[row2][col2])
        
        return "".join(decrypted_text)