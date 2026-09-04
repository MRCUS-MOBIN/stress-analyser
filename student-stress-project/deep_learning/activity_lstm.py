import torch
import torch.nn as nn

class ActivityLSTM(nn.Module):
    """
    LSTM Neural Network to analyze sequential student activity patterns 
    (sleep, study hours, screen time, physical activity, academic workload, social activity)
    over a multi-day window (e.g., 7 days).
    """
    def __init__(self, input_dim=6, hidden_dim=64, num_layers=2, output_dim=64, dropout=0.2):
        super(ActivityLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, output_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        # x shape: (batch_size, seq_len, input_dim)
        lstm_out, (h_n, c_n) = self.lstm(x)
        # Use final hidden state from top layer
        last_hidden = h_n[-1]
        embeddings = self.fc(last_hidden)
        return embeddings

if __name__ == "__main__":
    model = ActivityLSTM(input_dim=6, hidden_dim=64, output_dim=64)
    dummy_input = torch.randn(8, 7, 6) # batch 8, 7 days, 6 metrics
    out = model(dummy_input)
    print("ActivityLSTM Output shape:", out.shape) # (8, 64)
