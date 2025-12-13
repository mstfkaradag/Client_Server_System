from .base import Cipher

class DesManual(Cipher):
    def __init__(self, key_text):
        self.key_bin = self._text_to_bin(key_text)[:10].ljust(10, '0')

        self.k1, self.k2 = self._generate_subkeys(self.key_bin)

    def _text_to_bin(self, text):
        binary_string = ""

        for ch in text:
            binary_representation = format(ord(ch), '08b')
            binary_string += binary_representation

        return binary_string
    
    def _bin_to_text(self, binary):
        chars = []
        for i in range(0, len(binary), 8):
            chars.append(binary[i : i + 8])

        result = ""
        for c in chars:
            result += chr(int(c, 2))

        return result
    
    def _permute(self, bits, mapping):
        result = ""
        for i in mapping:
            result += bits[i - 1]
        return result
    
    def _left_shifts(self, bits, n):
        return bits[n:] + bits[:n]
    
    def _xor(self, bits1, bits2):
        result = ""
        for b1, b2 in zip(bits1, bits2):
            if b1 != b2:
                result += "1"
            else:
                result += "0"
        return result
    
    def _generate_subkeys(self, key_10bit):
        p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        key = self._permute(key_10bit, p10)

        left = key[:5]
        right = key[5:]
        
        left = self._left_shifts(left, 1)
        right = self._left_shifts(right, 1)

        p8 = [6, 3, 7, 4, 8, 5, 10, 9]
        k1 = self._permute(left + right, p8)

        left = self._left_shifts(left, 2)
        right = self._left_shifts(right, 2)

        k2 = self._permute(left + right, p8)

        return k1, k2
    
    def _feistel_function(self, right_4bit, subkey):
        ep = [4, 1, 2, 3, 2, 3, 4, 1]
        expanded = self._permute(right_4bit, ep)

        xored = self._xor(expanded, subkey)

        left_bits = xored[:4]
        right_bits = xored[4:]

        s0_matrix = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 3, 2]
        ]
        s1_matrix = [
            [0, 1, 2, 3],
            [2, 0, 1, 3],
            [3, 0, 1, 0],
            [2, 1, 0, 3]
        ]

        row0 = int(left_bits[0] + left_bits[3], 2)
        col0 = int(left_bits[1] + left_bits[2], 2)
        val0 = s0_matrix[row0][col0]
        out0 = format(val0, '02b')

        row1 = int(right_bits[0] + right_bits[3], 2)
        col1 = int(right_bits[1] + right_bits[2], 2)
        val1 = s1_matrix[row1][col1]
        out1 = format(val1, '02b')

        p4 = [2, 4, 3, 1]
        return self._permute(out0 + out1, p4)
    
    def _run_sdes(self, block_8bit, key1, key2):
        ip = [2, 6, 3, 1, 4, 8, 5, 7]
        permuted = self._permute(block_8bit, ip)

        left = permuted[:4]
        right = permuted[4:]

        f_result = self._feistel_function(right, key1)
        left = self._xor(left, f_result)

        left, right = right, left

        f_result = self._feistel_function(right, key2)
        left = self._xor(left, f_result)

        ip_inv = [4, 1, 3, 5, 7, 2, 8, 6]
        return self._permute(left + right, ip_inv)
    
    def encrypt(self, text):
        result = ""
        bin_text = self._text_to_bin(text)

        for i in range(0, len(bin_text), 8):
            block = bin_text[i : i + 8]
            encrypted_block = self._run_sdes(block, self.k1, self.k2)
            result += encrypted_block

        return result
    
    def decrypt(self, text):
        result = ""

        clean_text = ""
        for c in text:
            if c in '01':
                clean_text += c

        for i in range(0, len(clean_text), 8):
            block = clean_text[i : i + 8]
            decrypted_block = self._run_sdes(block, self.k2, self.k1)
            result += decrypted_block

        return self._bin_to_text(result)