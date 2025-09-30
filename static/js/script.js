async function processMessage() {
    const mode = document.getElementById('mode').value;
    const method = document.getElementById('method').value;
    const key = document.getElementById('key').value;
    const message = document.getElementById('message').value;

    const endpoint = mode === 'client' ? '/encrypt' : 'decrypt';

    try{
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({method, key, message})
        });

        const data = await response.json();
        const resultField = mode === 'client' ? 'encrypted_message' : 'decrypted_message';
        document.getElementById('result').value = data[resultField];
    }
    catch(error){
        alert("Hata oluştu: " + error);
    }
}