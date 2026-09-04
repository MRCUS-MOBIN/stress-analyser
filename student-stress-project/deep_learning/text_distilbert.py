import torch
import torch.nn as nn
import numpy as np

class TextSentimentEncoder(nn.Module):
    """
    DistilBERT-based / NLP neural encoder for extracting emotional and contextual
    information from student text-based self-expression / journal entries.
    """
    def __init__(self, embedding_dim=64, vocab_size=5000):
        super(TextSentimentEncoder, self).__init__()
        self.embedding_dim = embedding_dim
        
        # Word embedding layer for fast text representation
        self.token_embedding = nn.Embedding(vocab_size, 32, padding_idx=0)
        self.conv1d = nn.Conv1d(32, 64, kernel_size=3, padding=1)
        self.global_pool = nn.AdaptiveAvgPool1d(1)
        
        # Sentiment projection
        self.fc_text = nn.Sequential(
            nn.Linear(64, embedding_dim),
            nn.ReLU(),
            nn.LayerNorm(embedding_dim)
        )
        
        # Keywords map for rule-based sentiment augmentation
        self.stress_keywords = {
            "exam": 0.8, "midterm": 0.9, "assignment": 0.6, "deadline": 0.7,
            "sleep": 0.7, "insomnia": 0.9, "tired": 0.8, "exhausted": 0.9,
            "anxious": 0.9, "overwhelmed": 0.95, "scared": 0.85, "placement": 0.9,
            "interview": 0.85, "alone": 0.7, "isolated": 0.8, "conflict": 0.75
        }

    def simple_tokenize(self, text):
        if not isinstance(text, str): return [0]
        words = text.lower().replace(".", "").replace(",", "").split()
        tokens = [abs(hash(w)) % 4999 + 1 for w in words]
        return tokens if tokens else [0]

    def extract_text_embedding(self, text_list):
        batch_size = len(text_list)
        seq_len = 32
        padded_tokens = torch.zeros((batch_size, seq_len), dtype=torch.long)
        
        for i, txt in enumerate(text_list):
            toks = self.simple_tokenize(txt)[:seq_len]
            if toks:
                padded_tokens[i, :len(toks)] = torch.tensor(toks, dtype=torch.long)
                
        # Forward pass through embedding + Conv1D
        x = self.token_embedding(padded_tokens) # (batch, seq_len, 32)
        x = x.transpose(1, 2) # (batch, 32, seq_len)
        x = torch.relu(self.conv1d(x)) # (batch, 64, seq_len)
        x = self.global_pool(x).squeeze(2) # (batch, 64)
        out = self.fc_text(x)
        return out

    def forward(self, text_input):
        if isinstance(text_input, list):
            return self.extract_text_embedding(text_input)
        elif isinstance(text_input, torch.Tensor):
            return self.fc_text(text_input)
        else:
            return self.extract_text_embedding([str(text_input)])

if __name__ == "__main__":
    encoder = TextSentimentEncoder(embedding_dim=64)
    sample_texts = [
        "I have three major midterms coming up and I feel anxious.",
        "Slept well today, feeling refreshed and confident."
    ]
    emb = encoder(sample_texts)
    print("TextSentimentEncoder Output shape:", emb.shape) # (2, 64)
