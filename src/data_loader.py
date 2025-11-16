# data_loader.py
import os
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer


script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
data_path = os.path.join(script_dir, '../data/data_processed/all_data.csv')


class GermanDocumentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        # Tokenize the text
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

# Load your data
df = pd.read_csv(data_path)
tokenizer = AutoTokenizer.from_pretrained('bert-base-german-cased')

# Create dataset
dataset = GermanDocumentDataset(
    texts=df['text'].tolist(),
    labels=df['label'].tolist(),
    tokenizer=tokenizer
)

# Create data loader
train_loader = DataLoader(dataset, batch_size=16, shuffle=True)