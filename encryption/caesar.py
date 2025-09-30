def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isupper():
            result = result + chr((ord(char) + shift - 65) % 26 + 65) #ascii de büyük harfler 65-90 arası // chr -> bir sayıyı karaktere çevirir
        elif char.islower():
            result = result + chr((ord(char) + shift -97) % 26 + 97) #ascii de küçük harfler 97-122 arası // ord -> karakterin ascii karşılığını verir
        else:
            result = result + char
    
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)