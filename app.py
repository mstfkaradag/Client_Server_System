from flask import Flask, request, render_template, jsonify
from encryption.caesar import caesar_encrypt, caesar_decrypt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods = ['POST'])
def encrypt():
    data = request.json
    message = data['message']
    key = int(data['key'])
    method = data['method']

    if method == 'caesar':
        result = caesar_encrypt(message, key)

    return jsonify({'encrypted_message': result})

@app.route('/decrypt', methods = ['POST'])
def decrypt():
    data = request.json
    message = data['message']
    key = int(data['key'])
    method = data['method']

    if method == 'caesar':
        result = caesar_decrypt(message, key)

    return jsonify({'decrypted_message': result})
    
if __name__ == '__main__':
    app.run(debug = True)