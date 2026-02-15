# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Set environment variables
# Replace "your-db" with your actual database name
ENV MONGO_URI="mongodb+srv://farmer_admin:Roronoa123@newmain.t1vt5ne.mongodb.net/?appName=NewMain"

# Expose ports
EXPOSE 8000 
EXPOSE 8501

# Run both FastAPI and Streamlit together
# Adjust paths if your app files are named differently
#CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]

# Run FastAPI & Streamlit (optional: you can run them separately too)
CMD uvicorn fastapi_worker:app --host 0.0.0.0 --port 8000
# For Streamlit, you can later use: streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
