import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class PriceLSTM(nn.Module):
    def __init__(self, input_size=3, hidden_size=64, num_layers=2, output_size=7):
        super(PriceLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # x shape: (batch, seq_len, input_size)
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :]) # Take the last time step
        return out

class PricePredictor:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        
    def prepare_data(self, df, commodity_name):
        # Filter for specific crop and sort by date
        data = df[df['Commodity'] == commodity_name].copy()
        data['Arrival_Date'] = pd.to_datetime(data['Arrival_Date'])
        data = data.sort_values('Arrival_Date').set_index('Arrival_Date')
        
        # Resample to daily to handle missing dates (interpolate)
        data = data['Modal_Price'].resample('D').mean().interpolate(method='linear').to_frame()
        
        # Feature Engineering: 7-day and 30-day Moving Averages
        data['MA7'] = data['Modal_Price'].rolling(window=7).mean()
        data['MA30'] = data['Modal_Price'].rolling(window=30).mean()
        data.dropna(inplace=True)
        
        scaled_data = self.scaler.fit_transform(data)
        return scaled_data

    def create_sequences(self, data, seq_length=60, pred_length=7):
        x, y = [], []
        for i in range(len(data) - seq_length - pred_length):
            x.append(data[i : i + seq_length])
            y.append(data[i + seq_length : i + seq_length + pred_length, 0]) # Predict Modal_Price
        return torch.tensor(np.array(x), dtype=torch.float32), torch.tensor(np.array(y), dtype=torch.float32)

    def train_model(self, x_train, y_train, epochs=50):
        self.model = PriceLSTM(input_size=x_train.shape[2])
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        for epoch in range(epochs):
            self.model.train()
            optimizer.zero_grad()
            outputs = self.model(x_train)
            loss = criterion(outputs, y_train)
            loss.backward()
            optimizer.step()
            if (epoch+1) % 10 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')