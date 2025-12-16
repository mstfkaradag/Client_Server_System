from .base import Cipher
import math

class HillCipher(Cipher):
    def __init__(self, key_string):
        try:
            self.key_matrix = self._parse_key(key_string)
            self.n = len(self.key_matrix)
            
            det = self._get_determinant(self.key_matrix)
            det = det % 26
            
            if math.gcd(det, 26) != 1:
                raise ValueError(f"Matrisin determinantı ({det}) 26 ile aralarında asal değil. Bu anahtar kullanılamaz!")
                
            self.inverse_matrix = self._get_matrix_inverse(self.key_matrix)
            
        except Exception as e:
            raise ValueError(f"Hill Anahtar Hatası: {str(e)}")

    def _parse_key(self, key_string):
        nums = [int(x) for x in key_string.strip().split()]
        size = int(math.sqrt(len(nums)))
        
        if size * size != len(nums):
            raise ValueError("Anahtar kare matris oluşturmalıdır (Örn: 4 sayı -> 2x2, 9 sayı -> 3x3).")
            
        return [nums[i*size:(i+1)*size] for i in range(size)]

    def _get_determinant(self, matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        elif len(matrix) == 3:
            return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
                    matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
                    matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))
        else:
            raise ValueError("Sadece 2x2 ve 3x3 matrisler destekleniyor.")

    def _mod_inverse(self, a, m):
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError(f"{a}'nın mod {m}'de tersi yoktur.")

    def _get_matrix_inverse(self, matrix):
        det = self._get_determinant(matrix)
        det_inv = self._mod_inverse(det, 26)
        
        n = len(matrix)
        adj = []
        
        if n == 2:
            adj = [
                [matrix[1][1], -matrix[0][1]],
                [-matrix[1][0], matrix[0][0]]
            ]
        elif n == 3:
            adj = [[0]*3 for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    minor = []
                    for r in range(3):
                        if r == i: continue
                        row = []
                        for c in range(3):
                            if c == j: continue
                            row.append(matrix[r][c])
                        minor.append(row)
                    
                    cofactor = ((-1)**(i+j)) * (minor[0][0]*minor[1][1] - minor[0][1]*minor[1][0])
                    adj[j][i] = cofactor
                    
        inv = []
        for i in range(n):
            row = []
            for j in range(n):
                val = (det_inv * adj[i][j]) % 26
                row.append(val)
            inv.append(row)
        return inv

    def _process(self, text, matrix):
        if not text:
            return ""
        text = text.upper().replace(" ", "")
        
        while len(text) % self.n != 0:
            text += 'X'
            
        result = ""
        for i in range(0, len(text), self.n):
            block = text[i:i+self.n]
            vector = [ord(c) - 65 for c in block]
            
            res_vector = []
            for r in range(self.n):
                val = 0
                for c in range(self.n):
                    val += matrix[r][c] * vector[c]
                res_vector.append(val % 26)
            
            result += "".join([chr(v + 65) for v in res_vector])
            
        return result

    def encrypt(self, text):
        return self._process(text, self.key_matrix)

    def decrypt(self, text):
        return self._process(text, self.inverse_matrix)