async function getBestMandi() {
    const crop = document.getElementById('mandi-crop').value;
    const box = document.getElementById('mandi-result');

    box.innerText = "🔍 Searching mandis...";

    const res = await fetch('/best-mandi', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ crop })
    });

    const data = await res.json();

    box.innerHTML = `
        🏪 ${data.market}<br>
        💰 ₹${data.price}
    `;
}
