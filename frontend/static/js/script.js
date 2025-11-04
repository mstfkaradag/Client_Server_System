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

    let socket = null;

    async function loadSocketIoClient() {
        return new Promise((resolve, reject) => {
            if (window.io) {
                return resolve();
            }
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
        if (method === "substitution") {
            alphabetGroup.style.display = "";
            keyInput.type = "text";
            keyLabel.textContent = "Büyük Harfler Alfabesi";
        }
        else{
            alphabetGroup.style.display = "none";
            alphabetInput.value = "";
            keyLabel.textContent = "Anahtar";
            if (method === "caesar") {
                keyInput.type = "number";
            }
            else{
                keyInput.type = "text";
            }
        }
    }

    methodSelect.addEventListener("change", handleMethodChange);
    handleMethodChange();

    function timeNow() {
        const d = new Date();
        const hh = String(d.getHours()).padStart(2, "0");
        const mm = String(d.getMinutes()).padStart(2, "0");
        return `${hh}:${mm}`;
    }

    function timeFromEpoch(epochMs) {
        try {
            const d = new Date(Number(epochMs));
            return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
        } 
        catch (e) {
            return timeNow();
        }
    }


    function appendMessage({id, sender, direction, cipher, method, alphabet, ts}) {
        const li = document.createElement("li");
        li.className = `message-item ${direction}`;
        li.dataset.cipher = cipher;
        li.dataset.method = method || "";
        if (alphabet) {
            li.dataset.alphabet = alphabet;
        }
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
    }

    function restoreCipher(id) {
        const li = document.getElementById(id);
        if (!li) {
            return;
        }
        const cipher = li.dataset.cipher;
        const content = li.querySelector(".msg-content");
        if (content) {
            content.textContent = cipher;
        }
        const restoreBtn = li.querySelector(".restore-btn");
        const decryptBtn = li.querySelector(".decrypt-btn");
        if (restoreBtn) {
            restoreBtn.style.display = "none";
        }
        if (decryptBtn) {
            decryptBtn.style.display = "";
        }
        li.dataset.decrypted = "false";
    }

    async function decryptSingleMessage(id) {
        const li = document.getElementById(id);
        if (!li) {
            return;
        }
        const cipher = li.dataset.cipher;
        const method = li.dataset.method || methodSelect.value;
        const alphabet = li.dataset.alphabet || alphabetInput.value;

        try{
            const payload = {message: cipher, method: method, key: keyInput.value || "", alphabet: alphabet};
            const resp = await fetch("/decrypt", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            });
            const json = await resp.json();
            if (!resp.ok) {
                alert(json.error || "Deşifreleme başarısız oldu");
                return;
            }
            const plaintext = json.decrypted_message;
            const content = li.querySelector(".msg-content");
            content.textContent = plaintext;
            li.dataset.decrypted = "true";
            li.querySelector(".decrypt-btn").style.display = "none";
            li.querySelector(".restore-btn").style.display = "";
        }
        catch(err){
            console.error(err);
            alert("Deşifreleme sırasında hata oluştu");
        }
    }

    async function toggleShowAllDecrypted() {
        const shouldShow = showDecrypted.checked;
        const items = Array.from(messageList.querySelectorAll(".message-item"));
        for (const li of items) {
            if (shouldShow) {
                if (li.dataset.decrypted === "true") {
                    continue;
                }
                const cipher = li.dataset.cipher;
                const method = li.dataset.method || methodSelect.value;
                const alphabet = li.dataset.alphabet || alphabetInput.value;
                try{
                    const resp = await fetch("/decrypt", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({message: cipher, method: method, key: keyInput.value || "", alphabet: alphabet}),
                    });
                    const json = await resp.json();
                    if (resp.ok && json.decrypted_message !== undefined) {
                        li.querySelector(".msg-content").textContent = json.decrypted_message;
                        li.dataset.decrypted = "true";
                        li.querySelector(".decrypt-btn").style.display = "none";
                        li.querySelector(".restore-btn").style.display = "";
                    }
                    else{
                        console.warn("Hata: ", json);
                    }
                }
                catch(e){
                    console.warn("Hata: ", e);
                }
            }
            else{
                restoreCipher(li.id);
            }
        }
    }

    showDecrypted.addEventListener("change", toggleShowAllDecrypted);

    async function processMessage() {
        const method = methodSelect.value;
        const key = keyInput.value;
        const message = messageInput.value.trim();
        const alphabet = alphabetInput.value;
        const usernameTemp = (usernameInput && usernameInput.value ? usernameInput.value.trim() : "user_guest");

        if (!message) {
            alert("Mesaj boş olamaz");
            return;
        }

        if (method === "caesar") {
            if (key === "" || isNaN(Number(key))) {
                alert("Anahtar bir sayı olmalıdır");
                return;
            }
        }
        if(method === "vigenere" || method === "playfair"){
            if(!key || key.trim() === ""){
                alert("Anahtar boş olamaz");
                return;
            }
        }
        if (method === "substitution") {
            if(!key || key.trim() === ""){
                alert("Büyük harfler alfabesi boş olamaz");
                return;
            }
            if (!alphabet || alphabet.trim() === "") {
                alert("Küçük harfler alfabesi boş bırakılamaz");
                return;
            }
        }
        
        try{
            const payload = {message: message, method: method, key: key, alphabet: alphabet};
            const resp = await fetch("/encrypt", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            });
            const json = await resp.json();
            if (!resp.ok) {
                alert(json.error || "Şifreleme isteği başarısız");
                return;
            }
            const cipher = json.encrypted_message;
            const id = "m-" + Date.now() + "-" + Math.floor(Math.random() * 10000);
            appendMessage({id, sender: usernameTemp, direction: "sent", cipher, method, alphabet, ts: timeNow()});
            if (socket) {
                socket.emit("send_cipher", {method: method, encrypted_message: cipher, sender: usernameTemp, ts: Date.now()});
            }
            else{
                console.warn("Socket bağlı değil");
            }
            messageInput.value = "";
        }
        catch(err){
            console.error(err);
            alert("Şifreleme isteği sırasında hata çıktı");
        }
    }

    function setupSocketHandlers() {
        if (!socket) {
            return;
        }
        socket.on("connect", () => {
            console.log("Socket.IO bağlı: ", socket.id);
        });
        socket.on("disconnect", () => {
            console.log("Socket.IO bağlantısı koptu");
        });
        socket.on("recv_cipher", (data) => {
            if (!data) {
                return;
            }
            const method = data.method || methodSelect.value;
            const cipher = data.encrypted_message || data.cipher || data.message || data;
            const id = "m-" + Date.now() + "-" + Math.floor(Math.random() * 10000);
            const ts = data.ts ? timeFromEpoch(data.ts) : timeNow();
            const sender = data.sender || "user_guest";
            appendMessage({id, sender:sender, direction: "received", cipher, method, alphabet: alphabetInput.value, ts: ts});
        });
    }

    function clearHistory(){
        messageList.innerHTML = "";
    }

    sendBtn.addEventListener("click", processMessage);
    clearHistoryBtn.addEventListener("click", clearHistory);

    (async function init() {
        try{
            await loadSocketIoClient();
            socket = window.io ? window.io() : null;
            if (!socket) {
                console.warn("Socket.IO global 'io' bulunamadı");
            }
            else{
                setupSocketHandlers();
            }
        }
        catch(err){
            console.warn("Socket.IO hatası: ", err);
        }
    })();
})();