const API_URL = "http://localhost:8000/ask?q=";

const inputBox  = document.getElementById("user-input");
const chatBox   = document.getElementById("chat-box");
const sendBtn   = document.getElementById("send-btn");

// Send on Enter key
inputBox.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function appendMessage(role, text) {
    const div = document.createElement("div");
    div.className = "message " + role;
    div.innerHTML = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
}

function setLoading(active) {
    sendBtn.disabled  = active;
    inputBox.disabled = active;
}

function sendMessage() {
    const text = inputBox.value.trim();
    if (!text) return;

    appendMessage("user", "<b>You:</b> " + escapeHtml(text));
    inputBox.value = "";
    setLoading(true);

    // Show typing indicator
    const typing = appendMessage("typing", "Vinci is thinking…");

    fetch(API_URL + encodeURIComponent(text))
        .then(res => {
            if (!res.ok) throw new Error("Server error: " + res.status);
            return res.json();
        })
        .then(data => {
            chatBox.removeChild(typing);
            const reply = data.answer || "No response received.";
            appendMessage("bot", "<b>Vinci:</b> " + formatReply(reply));
        })
        .catch(err => {
            chatBox.removeChild(typing);
            appendMessage("bot", "<b>Error:</b> Could not reach Vinci backend. Make sure the server is running.");
            console.error(err);
        })
        .finally(() => {
            setLoading(false);
            inputBox.focus();
        });
}

function escapeHtml(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

function formatReply(text) {
    // Preserve line breaks in response
    return escapeHtml(text).replace(/\n/g, "<br>");
}
