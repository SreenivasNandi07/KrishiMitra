const express = require('express');
const axios = require('axios'); // You'll need to run: npm install axios
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static('public')); // This is where your frontend lives

// THE MAIN BRIDGE: Talk to FastAPI
app.post('/ask-ai', async (req, res) => {
    try {
        // req.body comes from your HTML (index.html)
        // It should contain { query: "your question", crop: "Wheat" }
        const response = await axios.post('http://127.0.0.1:8000/ask-ai', {
            query: req.body.query, 
            crop: req.body.crop || "Wheat" 
        });
        res.json(response.data);
    } catch (error) {
        console.error("Error connecting to Python:", error.message);
        res.status(500).json({ answer: "I'm having trouble connecting to my specialists. Please check if the Python server is running!" });
    }
});

app.listen(PORT, () => {
    console.log(`✅ Node.js Bridge running at http://localhost:${PORT}`);
});

