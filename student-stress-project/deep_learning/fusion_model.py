import torch
import torch.nn as nn
from deep_learning.activity_lstm import ActivityLSTM
from deep_learning.text_distilbert import TextSentimentEncoder

class MultimodalStressFusion(nn.Module):
    """
    Multimodal Fusion Neural Network combining:
    1. Sequential Student Activity patterns via ActivityLSTM
    2. Text Self-Expression & Emotional Context via DistilBERT / TextSentimentEncoder
    3. Emotion & Routine features (mood, anxiety, routine consistency)
    
    Produces detailed Stress Profile: Severity Score, Stress Nature, and Stress Trajectory.
    """
    def __init__(self, activity_dim=6, emotion_dim=3, hidden_dim=128, dropout=0.2):
        super(MultimodalStressFusion, self).__init__()
        
        self.lstm_branch = ActivityLSTM(input_dim=activity_dim, hidden_dim=64, output_dim=64)
        self.text_branch = TextSentimentEncoder(embedding_dim=64)
        
        self.emotion_fc = nn.Sequential(
            nn.Linear(emotion_dim, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32)
        )
        
        # Fused vector dimension: 64 (LSTM) + 64 (Text) + 32 (Emotion) = 160
        fused_dim = 64 + 64 + 32
        
        self.fusion_fc = nn.Sequential(
            nn.Linear(fused_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        # Multi-task Heads
        # Head 1: Stress Severity Score (0-100)
        self.severity_head = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
        
        # Head 2: Stress Nature Classification (6 categories)
        # Academic, Performance, Time-pressure, Sleep-related, Social, Mixed
        self.nature_head = nn.Linear(64, 6)
        
        # Head 3: Stress Trajectory (4 categories)
        # Stable, Increasing, Decreasing, Sudden Escalation
        self.trajectory_head = nn.Linear(64, 4)

    def forward(self, seq_activity, journal_texts, emotion_feats):
        """
        seq_activity: (batch, seq_len, 6)
        journal_texts: list of strings (len=batch) or pre-embedded tensor
        emotion_feats: (batch, 3) -> [anxiety_level, mood_rating, routine_consistency]
        """
        lstm_emb = self.lstm_branch(seq_activity)
        text_emb = self.text_branch(journal_texts)
        emotion_emb = self.emotion_fc(emotion_feats)
        
        # Multimodal Concatenation
        fused = torch.cat([lstm_emb, text_emb, emotion_emb], dim=1)
        fusion_rep = self.fusion_fc(fused)
        
        severity_score = self.severity_head(fusion_rep).squeeze(1)
        nature_logits = self.nature_head(fusion_rep)
        trajectory_logits = self.trajectory_head(fusion_rep)
        
        return {
            "severity_score": severity_score,
            "nature_logits": nature_logits,
            "trajectory_logits": trajectory_logits,
            "fusion_rep": fusion_rep
        }

if __name__ == "__main__":
    fusion_net = MultimodalStressFusion()
    batch_seq = torch.randn(4, 7, 6)
    texts = ["Exams tomorrow, extremely stressed.", "Slept 8 hours, feeling ready."] * 2
    emotions = torch.tensor([[8.0, 3.0, 5.0], [2.0, 9.0, 8.0]] * 2)
    
    out = fusion_net(batch_seq, texts, emotions)
    print("Multimodal Fusion Severity Scores:", out["severity_score"].detach().numpy())
    print("Nature Logits shape:", out["nature_logits"].shape)
    print("Trajectory Logits shape:", out["trajectory_logits"].shape)
