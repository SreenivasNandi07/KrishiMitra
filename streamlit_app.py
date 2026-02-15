'''import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="AgriMind AI", layout="centered")

st.title("🌾 AgriMind AI Assistant")

query = st.text_input(
    "Ask about crop prices, best mandi, or storage advice",
    placeholder="e.g. Should I store onion this week?"
)

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a query")
    else:
        try:
            res = requests.post(
                f"{API}/ask-ai",
                json={"query": query},
                timeout=30
            )
            st.success("Response received")
            st.write(res.json()["answer"])
        except Exception as e:
            st.error("Backend not reachable")
'''

import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="AgriMind AI", layout="wide")
st.title("🌾 AgriMind Farmer Dashboard")

tabs = st.tabs([
    "🤖 AgriMind AI",
    "📈 Price Predictor",
    "🏪 Best Mandi",
    "📊 Demand Trend",
    "🧺 Storage Advisor"
])

# -------------------------
# 🤖 AI Assistant
# -------------------------
with tabs[0]:
    st.subheader("Ask AgriMind AI")

    # 🌐 Language selector
    language = st.selectbox("Choose language", ["English", "Hindi", "Telugu"], index=0)

    # User query input
    q = st.text_input("Ask a question", key="ai")

    # Single button handling
    if st.button("Ask AI"):
        if not q.strip():
            st.warning("Please enter a question.")
        else:
            try:
                # send query and language to backend
                r = requests.post(f"{API}/ask-ai", json={"query": q, "language": language})
                r.raise_for_status()  # raise error for HTTP issues
                data = r.json()       # parse JSON
                st.write(data.get("answer"))
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
            except ValueError:
                st.error("Invalid response from API. Is your backend running?")
# -------------------------
# 📈 Price Predictor
# -------------------------
with tabs[1]:
    st.subheader("📈 7-Day Price Forecast")

    crop = st.text_input("Enter crop name", key="price")

    if st.button("Predict Price"):
        r = requests.post(f"{API}/predict-price", json={"query": crop})
        data = r.json()

        if "predicted_prices_next_7_days" in data:
            prices = data["predicted_prices_next_7_days"]

            st.line_chart(prices)

            change_pct = ((prices[-1] - prices[0]) / prices[0]) * 100

            if change_pct > 0:
                st.success(f"⬆ Price increasing by {change_pct:.2f}%")
            else:
                st.warning(f"⬇ Price decreasing by {abs(change_pct):.2f}%")

        else:
            st.error(data.get("error"))

# -------------------------
# 🏪 Best Mandi
# -------------------------
with tabs[2]:
    st.subheader("Best Mandi Recommendation")
    crop = st.text_input("Enter crop", key="mandi")

    if st.button("Find Best Mandi"):
        r = requests.post(f"{API}/best-mandi", json={"query": crop})
        st.json(r.json())

# -------------------------
# 📊 Demand Trend
# -------------------------
with tabs[3]:
    st.subheader("Demand Trend (via AI)")
    crop = st.text_input("Enter crop", key="demand")

    if st.button("Check Demand"):
        r = requests.post(
            f"{API}/ask-ai",
            json={"query": f"demand trend for {crop}"}
        )
        st.write(r.json()["answer"])

# -------------------------
# 🧺 Storage Advisor
# -------------------------
with tabs[4]:
    st.subheader("Storage Recommendation")
    crop = st.text_input("Enter crop", key="storage")

    if st.button("Get Advice"):
        r = requests.post(
            f"{API}/ask-ai",
            json={"query": f"Should I store or sell {crop}?"}
        )
        st.write(r.json()["answer"])
