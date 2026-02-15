async function getStorageAdvice() {
    const crop = document.getElementById('storage-crop').value;

    const signal = document.getElementById('storage-signal');
    const text = document.getElementById('storage-text');

    signal.innerText = "⏳ Analyzing...";
    text.innerText = "";

    const res = await fetch('/storage-advice', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ crop })
    });

    const data = await res.json();

    if (data.signal === "SELL") {
        signal.innerText = "SELL NOW";
        signal.style.color = "red";
    } else {
        signal.innerText = "STORE";
        signal.style.color = "green";
    }

    text.innerText = data.reason;
}
