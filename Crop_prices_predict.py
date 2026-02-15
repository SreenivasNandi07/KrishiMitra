# works well
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class PriceLSTM(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size, 64, 2, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(64, 7)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

class PricePredictor:
    def __init__(self):
        self.scaler = MinMaxScaler()

    def prepare_data(self, df, crop):
        data = df[df["Commodity"] == crop].copy()
        if len(data) < 100:
            raise ValueError("Not enough data for prediction")

        data["Arrival_Date"] = pd.to_datetime(data["Arrival_Date"])
        data = data.sort_values("Arrival_Date").set_index("Arrival_Date")

        data = data["Modal_Price"].resample("D").mean().interpolate()
        data = data.to_frame()

        data["MA7"] = data["Modal_Price"].rolling(7).mean()
        data["MA30"] = data["Modal_Price"].rolling(30).mean()
        data.dropna(inplace=True)

        return self.scaler.fit_transform(data)

    def create_sequences(self, data, seq_len=60):
        X, y = [], []
        for i in range(len(data) - seq_len - 7):
            X.append(data[i:i+seq_len])
            y.append(data[i+seq_len:i+seq_len+7, 0])
        return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

    def predict(self, df, crop):
        data = self.prepare_data(df, crop)
        X, y = self.create_sequences(data)

        model = PriceLSTM(X.shape[2])
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        loss_fn = nn.MSELoss()

        for _ in range(25):
            optimizer.zero_grad()
            loss = loss_fn(model(X), y)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            pred = model(X[-1:].clone()).numpy()[0]

        min_, max_ = self.scaler.data_min_[0], self.scaler.data_max_[0]
        return (pred * (max_ - min_) + min_).tolist()
"""
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class PriceLSTM(nn.Module):
    def __init__(self, input_size=3, hidden_size=64, num_layers=2, output_size=7):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

class PricePredictor:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()

    def prepare_data(self, df, crop):
        # 🔑 normalize columns ONCE
        df = df.copy()
        df.columns = df.columns.str.lower()

        data = df[df["commodity"] == crop].copy()
        if data.empty:
            raise ValueError(f"No data found for crop: {crop}")

        data["arrival_date"] = pd.to_datetime(data["arrival_date"])
        data = data.sort_values("arrival_date").set_index("arrival_date")

        data = data["modal_price"].resample("D").mean().interpolate()

        data = pd.DataFrame({
            "price": data,
            "ma7": data.rolling(7).mean(),
            "ma30": data.rolling(30).mean()
        }).dropna()

        scaled = self.scaler.fit_transform(data)
        return scaled

    def create_sequences(self, data, seq_len=60, pred_len=7):
        X, y = [], []
        for i in range(len(data) - seq_len - pred_len):
            X.append(data[i:i+seq_len])
            y.append(data[i+seq_len:i+seq_len+pred_len, 0])
        return torch.tensor(np.array(X), dtype=torch.float32), torch.tensor(np.array(y), dtype=torch.float32)

    def train_model(self, X, y, epochs=10):
        self.model = PriceLSTM(input_size=X.shape[2])
        opt = torch.optim.Adam(self.model.parameters(), lr=0.001)
        loss_fn = nn.MSELoss()

        for _ in range(epochs):
            opt.zero_grad()
            loss = loss_fn(self.model(X), y)
            loss.backward()
            opt.step()
"""