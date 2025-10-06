from flask import Flask, request, render_template, jsonify
from encryption.caesar import CaesarCipher
from encryption.vigenere import VigenereCipher

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods = ['POST'])
def encrypt():
    data = request.json
    message = data['message']
    method = data['method']

    if method == 'caesar':
        key = int(data['key'])
        result = CaesarCipher(key)
        result_text = result.encrypt(message)
    elif method == 'vigenere':
        key = data['key']
        result = VigenereCipher(key)
        result_text = result.encrypt(message)

    return jsonify({'encrypted_message': result_text})

@app.route('/decrypt', methods = ['POST'])
def decrypt():
    data = request.json
    message = data['message']
    method = data['method']

    if method == 'caesar':
        key = int(data['key'])
        result = CaesarCipher(-key)
        result_text = result.encrypt(message)
    elif method == 'vigenere':
        key = data['key']
        result = VigenereCipher(key)
        result_text = result.decrypt(message)


    return jsonify({'decrypted_message': result_text})
    
if __name__ == '__main__':
    app.run(debug = True)