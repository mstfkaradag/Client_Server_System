import math

class Playfair():
    def __init__(self, key):
        key = key.upper()
        key = key.replace("J", "I")
        result = ""
        seen = set()
        for c in key:
            if c not in seen:
                result += c
                seen.add(c)
        self.key = result

    def key_square_matrix(self):
        matrix = [
            ["A", "B", "C", "D", "E"],
            ["F", "G", "H", "I", "K"],
            ["L", "M", "N", "O", "P"],
            ["Q", "R", "S", "T", "U"],
            [ "V", "W", "X", "Y", "Z"]
        ]

        new_matrix = [
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', '']
        ]

        index = 0
        while index != len(self.key):
            for i in range(5):
                for j in range(5):
                    if self.key[index] == matrix[i][j]:
                        matrix[i][j] = "0"
            index += 1
        
        index = 0
        for i in range(5):
            for j in range(5):
                if index < len(self.key):
                    new_matrix[i][j] = self.key[index]
                    index += 1
                else:
                    break

        index = len(self.key) // 5
        mod = len(self.key) % 5

        for i in range(5):
            for j in range(5):
                if matrix[i][j] != "0":
                    new_matrix[index][mod] = matrix[i][j]
                    mod += 1
                    if mod == 5:
                        mod = 0
                        index += 1
                        if index == 5:
                            break
                else:
                    continue
            if index == 5:
                break

        self.alphabet_matrix = new_matrix

    def alphabet_location(self, letter):
        for i in range(5):
            for j in range(5):
                if self.alphabet_matrix[i][j] == letter:
                    return i, j

    def encrypt(self, text):
        self.key_square_matrix()
        text = text.replace(" ", "")
        text = text.upper()
        text = text.replace("J", "I")
        result = ""

        index = 0
        word_groups = []
        while index < len(text):
            if index == len(text) - 1:
                word_groups.append(text[index] + 'X')
                break
            elif text[index] == text[index + 1]:
                word_groups.append(text[index] + 'X')
                index += 1
            else:
                word_groups.append(text[index] + text[index + 1])
                index += 2
        

        cycle = math.ceil(len(text) / 2)
        for i in range(cycle):
            row, col = self.alphabet_location(word_groups[i][0])
            row_other, col_other = self.alphabet_location(word_groups[i][1])
            if row == row_other:
                if col == 4:
                    result = result + self.alphabet_matrix[row][0]
                elif col != 4:
                    result = result + self.alphabet_matrix[row][col + 1]
                
                if col_other == 4:
                    result = result + self.alphabet_matrix[row_other][0]
                elif col_other != 4:
                    result = result + self.alphabet_matrix[row_other][col_other + 1]

            elif col == col_other:
                if row == 4:
                    result = result + self.alphabet_matrix[0][col]
                elif row != 4:
                    result = result + self.alphabet_matrix[row + 1][col]

                if row_other == 4:
                    result = result + self.alphabet_matrix[0][col_other]
                elif row_other != 4:
                    result = result + self.alphabet_matrix[row_other + 1][col_other]

            else:
                result = result + self.alphabet_matrix[row][col_other]
                result = result + self.alphabet_matrix[row_other][col]

        return result

    def decrypt(self, text):
        self.key_square_matrix()
        text = text.replace(" ", "")
        text = text.upper()
        result = ""

        index = 0
        word_groups = []
        while index < len(text):
            word_groups.append(text[index] + text[index + 1])
            index += 2

        cycle = math.ceil(len(text) / 2)
        for i in range(cycle):
            row, col = self.alphabet_location(word_groups[i][0])
            row_other, col_other = self.alphabet_location(word_groups[i][1])
            if row == row_other:
                if col == 0:
                    result = result + self.alphabet_matrix[row][4]
                elif col != 0:
                    result = result + self.alphabet_matrix[row][col - 1]
                
                if col_other == 0:
                    result = result + self.alphabet_matrix[row_other][4]
                elif col_other != 0:
                    result = result + self.alphabet_matrix[row_other][col_other - 1]

            elif col == col_other:
                if row == 0:
                    result = result + self.alphabet_matrix[4][col]
                elif row != 0:
                    result = result + self.alphabet_matrix[row - 1][col]

                if row_other == 0:
                    result = result + self.alphabet_matrix[4][col_other]
                elif row_other != 0:
                    result = result + self.alphabet_matrix[row_other - 1][col_other]

            else:
                result = result + self.alphabet_matrix[row][col_other]
                result = result + self.alphabet_matrix[row_other][col]

        return result