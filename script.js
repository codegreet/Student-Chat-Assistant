const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

sendBtn.addEventListener('click', async () => {
    const question = userInput.value.trim();
    if (!question) return;

    // Show user message
    chatbox.innerHTML += `<div class="user"><b>You:</b> ${question}</div>`;
    userInput.value = '';

    try {
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        chatbox.innerHTML += `<div class="bot"><b>Bot:</b> ${data.answer}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    } catch (err) {
        chatbox.innerHTML += `<div class="bot"><b>Bot:</b> Error connecting to server.</div>`;
    }
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendBtn.click();
});