async function predictPrice() {
    const crop = document.getElementById('price-crop').value;
    const result = document.getElementById('price-result');

    result.innerHTML = "📊 Predicting...";

    const res = await fetch('/predict-price', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ crop })
    });

    const data = await res.json();

    result.innerHTML = `
        <b>Next 7 Days Avg:</b> ₹${data.avg_price}<br>
        <b>Model Accuracy:</b> ${data.accuracy}%
    `;

    // You can later draw chart here
}
