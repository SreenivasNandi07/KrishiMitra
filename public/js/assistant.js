async function askAI() {
    const input = document.getElementById('ai-input');
    const chat = document.getElementById('ai-chat');

    chat.innerHTML += `<div>🌱 You: ${input.value}</div>`;

    const res = await fetch('/ask-ai', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ query: input.value })
    });

    const data = await res.json();

    chat.innerHTML += `<div>🤖 AI: ${data.answer}</div>`;
    input.value = "";
}
