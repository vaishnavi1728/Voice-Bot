// Use localhost (not 127.0.0.1) to avoid IPv6 mismatch on some Windows setups
const API_URL = "https://voice-bot-1-oult.onrender.com";

let recognition;
if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
} else {
    alert("Your browser does not support Speech Recognition. Use Chrome or Edge.");
}

document.getElementById("startBtn").onclick = () => {
    try {
        recognition.start();
    } catch (e) {
        // If recognition is not ready
        console.error(e);
    }
};

recognition.onresult = async (event) => {
    const text = event.results[0][0].transcript;
    document.getElementById("userText").innerText = text;

    try {
        console.log("Sending to backend:", API_URL, text);
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            const txt = await response.text();
            console.error("Backend returned non-OK:", response.status, txt);
            document.getElementById("botText").innerText = "Server error.";
            return;
        }

        const data = await response.json();
        console.log("Backend returned:", data);
        document.getElementById("botText").innerText = data.response || "No response.";
    } catch (err) {
        console.error("Fetch failed:", err);
        document.getElementById("botText").innerText = "Network error: " + err.toString();
    }
};

document.getElementById("speakBtn").onclick = () => {
    const text = document.getElementById("botText").innerText || "No response to speak";
    const msg = new SpeechSynthesisUtterance(text);
    msg.lang = "en-US";
    window.speechSynthesis.speak(msg);
};
5
