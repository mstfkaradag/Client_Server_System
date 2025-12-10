(function(){
    const methodSelect = document.getElementById('method');
    const alphabetGroup = document.getElementById('alphabetGroup');
    const alphabetInput = document.getElementById('alphabet');
    const keyInput = document.getElementById('key');
    const keyLabel = document.getElementById('keyLabel');
    const showDecrypted = document.getElementById('showDecrypted');
    const messageList = document.getElementById('messageList');
    const messageInput = document.getElementById('message');
    const sendBtn = document.getElementById('sendBtn');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    const usernameInput = document.getElementById('username');
    const genKeyBtn = document.getElementById('genKeyBtn');
    const privateKeyGroup = document.getElementById('privateKeyGroup');
    const privateKeyInput = document.getElementById('privateKey');

    let socket = null;

    async function loadSocketIoClient() {
        return new Promise((resolve, reject) => {
            if (window.io) return resolve();
            const s = document.createElement("script");
            s.src = "https://cdn.socket.io/4.8.1/socket.io.min.js";
            s.async = true;
            s.onload = () => resolve();
            s.onerror = () => reject(new Error("Socket.IO client yüklenemedi"));
            document.head.appendChild(s);
        });
    }

    function handleMethodChange() {
        const method = methodSelect.value;
        
        alphabetGroup.style.display = "none";
        privateKeyGroup.style.display = "none";
        genKeyBtn.style.display = "none";
        keyInput.type = "text";
        keyLabel.textContent = "Anahtar";
        keyInput.placeholder = "Anahtar giriniz...";

        if (method === "substitution") {
            alphabetGroup.style.display = "";
            keyLabel.textContent = "Büyük Harfler Alfabesi";
        }
        else if (method === "caesar") {
            keyInput.type = "number";
            keyLabel.textContent = "Kaydırma Miktarı (Sayı)";
        }
        else if (method === "rsa-with-lib") {
            keyLabel.textContent = "Public Key (Şifreleme İçin)";
            keyInput.placeholder = "Public Key buraya...";
            genKeyBtn.style.display = "block";
            privateKeyGroup.style.display = "block";
        }
        else if (method.includes("aes") || method.includes("des")) {
            keyLabel.textContent = `Anahtar (${method.includes("aes") ? "16" : "8"} karakter)`;
        }
    }

    methodSelect.addEventListener("change", handleMethodChange);
    handleMethodChange();

    window.generateRSAKeys = async function() {
        genKeyBtn.textContent = "Üretiliyor...";
        genKeyBtn.disabled = true;
        try {
            const resp = await fetch("/generate-keys");
            const json = await resp.json();
            if(json.error) {
                alert("Hata: " + json.error);
            } else {
                keyInput.value = json.public_key;
                privateKeyInput.value = json.private_key;
            }
        } catch(e) {
            alert("Anahtar üretilirken hata oluştu");
            console.error(e);
        } finally {
            genKeyBtn.textContent = "RSA Anahtar Çifti Oluştur";
            genKeyBtn.disabled = false;
        }
    };

    function timeNow() {
        const d = new Date();
        return `${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`;
    }

    function timeFromEpoch(epochMs) {
        try {
            const d = new Date(Number(epochMs));
            return `${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`;
        } catch (e) { return timeNow(); }
    }

    function appendMessage({id, sender, direction, cipher, method, alphabet, ts}) {
        const li = document.createElement("li");
        li.className = `message-item ${direction}`;
        li.dataset.cipher = cipher;
        li.dataset.method = method || "";
        if (alphabet) li.dataset.alphabet = alphabet;
        li.id = id;

        const header = document.createElement("div");
        header.className = "msg-header";
        const you = (usernameInput && usernameInput.value ? usernameInput.value.trim() : "user_guest");
        let headerText = sender ? sender : (direction === "sent" ? you : "user_guest");
        if (direction === "sent" && headerText === you) headerText += " (siz)";
        headerText += ` • ${ts || timeNow()}`;
        header.textContent = headerText;

        const content = document.createElement("pre");
        content.className = "msg-content";
        content.textContent = cipher;

        const controls = document.createElement("div");
        controls.className = "msg-controls";

        const decryptBtn = document.createElement("button");
        decryptBtn.textContent = "Deşifre et";
        decryptBtn.className = "decrypt-btn";
        decryptBtn.addEventListener("click", () => decryptSingleMessage(id));

        const restoreBtn = document.createElement("button");
        restoreBtn.textContent = "Şifrele";
        restoreBtn.className = "restore-btn";
        restoreBtn.style.display = "none";
        restoreBtn.addEventListener("click", () => restoreCipher(id));

        controls.appendChild(decryptBtn);
        controls.appendChild(restoreBtn);

        li.appendChild(header);
        li.appendChild(content);
        li.appendChild(controls);

        messageList.appendChild(li);
        messageList.scrollTop = messageList.scrollHeight;
        
        if (showDecrypted.checked) {
             decryptSingleMessage(id);
        }
    }

    function restoreCipher(id) {
        const li = document.getElementById(id);
        if (!li) return;
        
        const cipher = li.dataset.cipher;
        li.querySelector(".msg-content").textContent = cipher;
        li.querySelector(".restore-btn").style.display = "none";
        li.querySelector(".decrypt-btn").style.display = "";
        li.dataset.decrypted = "false";
    }

    async function decryptSingleMessage(id) {
        const li = document.getElementById(id);
        if (!li) return;

        const cipher = li.dataset.cipher;
        const method = li.dataset.method || methodSelect.value;
        const alphabet = li.dataset.alphabet || alphabetInput.value;
        
        let keyToSend = keyInput.value || "";
        if (method === "rsa-with-lib") {
            keyToSend = privateKeyInput.value || "";
            if(!keyToSend) {
                alert("RSA mesajını çözmek için Private Key gerekli!");
                return;
            }
        }

        try {
            const payload = {
                message: cipher, 
                method: method, 
                key: keyToSend, 
                alphabet: alphabet
            };
            
            const resp = await fetch("/decrypt", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            });
            
            const json = await resp.json();
            if (!resp.ok) {
                console.warn(json.error);
                return;
            }
            
            const plaintext = json.decrypted_message;
            li.querySelector(".msg-content").textContent = plaintext;
            li.dataset.decrypted = "true";
            li.querySelector(".decrypt-btn").style.display = "none";
            li.querySelector(".restore-btn").style.display = "";
        } catch(err) {
            console.error(err);
        }
    }

    async function processMessage() {
        const method = methodSelect.value;
        const key = keyInput.value;
        const message = messageInput.value.trim();
        const alphabet = alphabetInput.value;
        const usernameTemp = usernameInput.value.trim() || "user_guest";

        if (!message) { alert("Mesaj boş olamaz"); return; }

        if (method === "caesar" && (key === "" || isNaN(Number(key)))) {
            alert("Sezar için sayısal anahtar gerekli"); return;
        }
        if (method === "rsa-with-lib" && !key) {
             alert("RSA için Public Key gerekli (Anahtar Oluştur butonunu kullanın)"); return;
        }
        
        try {
            const payload = {message, method, key, alphabet};
            
            const resp = await fetch("/encrypt", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            });
            
            const json = await resp.json();
            if (!resp.ok) {
                alert(json.error || "Şifreleme başarısız");
                return;
            }
            
            const cipher = json.encrypted_message;
            const id = "m-" + Date.now() + "-" + Math.floor(Math.random() * 10000);
            
            appendMessage({
                id, 
                sender: usernameTemp, 
                direction: "sent", 
                cipher, 
                method, 
                alphabet, 
                ts: timeNow()
            });
            
            if (socket) {
                socket.emit("send_cipher", {
                    method: method, 
                    encrypted_message: cipher, 
                    sender: usernameTemp, 
                    ts: Date.now()
                });
            } else {
                console.warn("Socket bağlı değil");
            }
            
            messageInput.value = "";
            
        } catch(err) {
            console.error(err);
            alert("İşlem sırasında hata oluştu");
        }
    }
    
    function setupSocketHandlers() {
        if (!socket) return;
        
        socket.on("connect", () => console.log("Bağlandı: ", socket.id));
        
        socket.on("recv_cipher", (data) => {
            if (!data) return;
            const method = data.method || "caesar";
            const cipher = data.encrypted_message || data.cipher;
            const id = "m-" + Date.now() + "-" + Math.floor(Math.random() * 10000);
            const ts = data.ts ? timeFromEpoch(data.ts) : timeNow();
            const sender = data.sender || "Anonim";
            
            appendMessage({
                id, 
                sender, 
                direction: "received", 
                cipher, 
                method, 
                alphabet: "",
                ts
            });
        });
    }

    function clearHistory(){ messageList.innerHTML = ""; }

    sendBtn.addEventListener("click", processMessage);
    clearHistoryBtn.addEventListener("click", clearHistory);
    showDecrypted.addEventListener("change", () => {
        const items = messageList.querySelectorAll(".message-item");
        if(showDecrypted.checked) {
            items.forEach(li => {
                if(li.dataset.decrypted !== "true") decryptSingleMessage(li.id);
            });
        } else {
            items.forEach(li => restoreCipher(li.id));
        }
    });

    (async function init() {
        try {
            await loadSocketIoClient();
            socket = window.io ? window.io() : null;
            if (socket) setupSocketHandlers();
        } catch(err) { console.warn("Socket hatası: ", err); }
    })();

})();