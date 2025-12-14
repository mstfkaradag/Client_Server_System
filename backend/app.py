import os
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from encryption.caesar import CaesarCipher
from encryption.vigenere import VigenereCipher
from encryption.substitution import SubstitutionCipher
from encryption.playfair import Playfair
from encryption.aes_lib import AesLib
from encryption.des_lib import DesLib
from encryption.rsa_lib import RsaLib
from encryption.des_manual import DesManual
from encryption.rail_fence import RailFenceCipher
from encryption.route import RouteCipher
from encryption.columnar import ColumnarTransposition

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder,"index.html")

def bad_request(msg):
    return jsonify({"error": msg}), 400

@app.route("/encrypt", methods = ["POST"])
def encrypt():
    if not request.is_json:
        return bad_request("İstek JSON olmalı")
    
    data = request.get_json()
    message = data.get("message")
    method = data.get("method")

    if not method:
        return bad_request("Method girmediniz")
    if message is None:
        return bad_request("Mesaj giriniz")

    try:
        if method == "caesar":
            key = data.get("key")
            if key is None:
                return bad_request("Key boş bırakılamaz")
            try:
                key = int(key)
            except ValueError:
                return bad_request("Key bir sayı olmalıdır")
            result = CaesarCipher(key)
            result_text = result.encrypt(message)
        elif method == "rail-fence":
            key = data.get("key")
            if key is None:
                return bad_request("Key boş bırakılamaz")
            try:
                key = int(key)
            except ValueError:
                return bad_request("Key bir sayı olmalıdır")
            result = RailFenceCipher(key)
            result_text = result.encrypt(message)
        elif method == "route":
            key = data.get("key")
            if key is None:
                return bad_request("Key boş bırakılamaz")
            try:
                key = int(key)
            except ValueError:
                return bad_request("Key bir sayı olmalıdır")
            result = RouteCipher(key)
            result_text = result.encrypt(message)
        elif method == "des-manual":
            key = data.get("key", "")
            if not isinstance(key, str) or key.strip() == "": 
                return bad_request("Key gerekli")
            result = DesManual(key)
            result_text = result.encrypt(message)
        elif method == "vigenere":
            key = data.get("key", "")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = VigenereCipher(key)
            result_text = result.encrypt(message)
        elif method == "columnar":
            key = data.get("key", "")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = ColumnarTransposition(key)
            result_text = result.encrypt(message)
        elif method == "substitution":
            key = data.get("key")
            alphabet = data.get("alphabet")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            if not isinstance(alphabet, str) or alphabet.strip() == "":
                return bad_request("Alfabe boş bırakılamaz")
            result = SubstitutionCipher(key, alphabet)
            result_text = result.encrypt(message)
        elif method == "playfair":
            key = data.get("key")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = Playfair(key)
            result_text = result.encrypt(message)
        elif method == "aes-with-lib":
            key = data.get("key", "")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = AesLib(key)
            result_text = result.encrypt(message)
        elif method == "des-with-lib":
            key = data.get("key", "")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = DesLib(key)
            result_text = result.encrypt(message)
        elif method == "rsa-with-lib":
            key = data.get("key", "")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = RsaLib(key)
            result_text = result.encrypt(message)
        else:
            return bad_request("Desteklenmeyen method")
        
    except Exception as e:
        return jsonify({"error": "Şifreleme esnasında hata oluştu: " + str(e)}), 400
    

    return jsonify({"encrypted_message": result_text})

@app.route("/decrypt", methods = ["POST"])
def decrypt():
    if not request.is_json:
        return bad_request("İstek JSON olmalı")
    
    data = request.get_json()
    message = data.get("message")
    method = data.get("method")

    if not method:
        return bad_request("Method girmediniz")
    if message is None:
        return bad_request("Mesaj giriniz")

    try:
        if method == "caesar":
            key = data.get("key")
            if key is None:
                return bad_request("Key boş bırakılamaz")
            try:
                key = int(key)
            except ValueError:
                return bad_request("Key bir sayı olmalıdır")
            result = CaesarCipher(key)
            result_text = result.decrypt(message)
        elif method == "rail-fence":
            key = data.get("key")
            if key is None:
                return bad_request("Key boş bırakılamaz")
            try:
                key = int(key)
            except ValueError:
                return bad_request("Key bir sayı olmalıdır")
            result = RailFenceCipher(key)
            result_text = result.decrypt(message)
        elif method == "route":
            key = data.get("key")
            if key is None:
                return bad_request("Key boş bırakılamaz")
            try:
                key = int(key)
            except ValueError:
                return bad_request("Key bir sayı olmalıdır")
            result = RouteCipher(key)
            result_text = result.decrypt(message)
        elif method == "columnar":
            key = data.get("key", "")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = ColumnarTransposition(key)
            result_text = result.decrypt(message)
        elif method == "des-manual":
            key = data.get("key", "")
            if not isinstance(key, str) or key.strip() == "": 
                return bad_request("Key gerekli")
            result = DesManual(key)
            result_text = result.decrypt(message)
        elif method == "vigenere":
            key = data.get("key", "")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = VigenereCipher(key)
            result_text = result.decrypt(message)
        elif method == "substitution":
            key = data.get("key")
            alphabet = data.get("alphabet")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            if not isinstance(alphabet, str) or alphabet.strip() == "":
                return bad_request("Alfabe boş bırakılamaz")
            result = SubstitutionCipher(key, alphabet)
            result_text = result.decrypt(message)
        elif method == "playfair":
            key = data.get("key")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = Playfair(key)
            result_text = result.decrypt(message)
        elif method == "aes-with-lib":
            key = data.get("key")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = AesLib(key)
            result_text = result.decrypt(message)
        elif method == "des-with-lib":
            key = data.get("key")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = DesLib(key)
            result_text = result.decrypt(message)
        elif method == "rsa-with-lib":
            key = data.get("key")
            if not isinstance(key, str) or key.strip() == "":
                return bad_request("Key boş bırakılamaz")
            result = RsaLib(key, is_private=True)
            result_text = result.decrypt(message)
        else:
            return bad_request("Desteklenmeyen method")
        
    except Exception as e:
        return jsonify({"error": "Deşifreleme esnasında hata oluştu: " + str(e)}), 400
    

    return jsonify({"decrypted_message": result_text})

@app.route("/generate-keys", methods=["GET"])
def generate_keys():
    try:
        private_k, public_k = RsaLib.generate_keys()
        return jsonify({
            "private_key": private_k,
            "public_key": public_k
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@socketio.on("send_cipher")
def handle_send_cipher(data):
    emit("recv_cipher", data, broadcast=True, include_self=False)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)