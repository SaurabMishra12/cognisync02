import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
import re

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', './cstm_rebuttal_output')
os.makedirs(f'{OUTPUT_DIR}/results/', exist_ok=True)

class MultiSignalDefense:
    def __init__(self, encoder):
        self.encoder = encoder
        self.classifier = None
        self.mean_clean_emb = None
        self.clean_docs = None

    def fit(self, clean_docs, ds):
        self.clean_docs = list(clean_docs)
        clean_embs = self.encoder.encode(self.clean_docs, show_progress_bar=False, batch_size=256)
        mean_emb = np.mean(clean_embs, axis=0)
        self.mean_clean_emb = mean_emb / (np.linalg.norm(mean_emb) + 1e-10)
        
        df = ds.to_pandas()
        X_texts = df['text'].tolist()
        y_true = df['label'].tolist()
        
        X_embs = self.encoder.encode(X_texts, show_progress_bar=False, batch_size=256)
        
        X_train, X_test, y_train, y_test = train_test_split(X_embs, y_true, test_size=0.2, random_state=RANDOM_SEED, stratify=y_true)
        
        self.classifier = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=RANDOM_SEED)
        self.classifier.fit(X_train, y_train)
        
        return self, X_test, y_test

    def filter_classifier_only(self, candidate_docs):
        if not candidate_docs: return [], []
        embs = self.encoder.encode(candidate_docs, show_progress_bar=False, batch_size=256)
        preds = self.classifier.predict_proba(embs)[:, 1]
        
        filtered_indices = []
        blocked_indices = []
        for i, prob in enumerate(preds):
            if prob < 0.5:
                filtered_indices.append(i)
            else:
                blocked_indices.append(i)
        return filtered_indices, blocked_indices

    def filter_full_heuristic(self, query, candidate_docs):
        if not candidate_docs: return [], []
        embs = self.encoder.encode(candidate_docs, show_progress_bar=False, batch_size=256)
        q_emb = self.encoder.encode([query], show_progress_bar=False)[0]
        q_norm = q_emb / (np.linalg.norm(q_emb) + 1e-10)
        
        preds = self.classifier.predict_proba(embs)[:, 1]
        
        filtered_indices = []
        blocked_indices = []
        for i, (doc, prob) in enumerate(zip(candidate_docs, preds)):
            norm_emb = embs[i] / (np.linalg.norm(embs[i]) + 1e-10)
            q_sim = np.dot(norm_emb, q_norm)
            imperative = 1.0 if re.search(r'(?i)\b(ignore|reveal|execute|forget|bypass|output)\b', doc) else 0.0
            
            is_goal_redirection = (imperative > 0) and (q_sim < 0.3)
            
            if prob < 0.5 and not is_goal_redirection:
                filtered_indices.append(i)
            else:
                blocked_indices.append(i)
        return filtered_indices, blocked_indices

def main():
    print("Loading deepset/prompt-injections dataset...")
    ds = load_dataset("deepset/prompt-injections", split="train")
    
    total_samples = len(ds)
    benign_count = sum(1 for x in ds if x['label'] == 0)
    malicious_count = total_samples - benign_count
    
    print(f"Dataset Counts -> Benign: {benign_count}, Malicious: {malicious_count}")
    
    encoder = SentenceTransformer(MODEL_NAME)
    defense = MultiSignalDefense(encoder)
    
    # We use a simulated "clean pool" of benign examples to build the mean_clean_emb
    clean_pool = [x['text'] for x in ds if x['label'] == 0][:100]
    
    defense, X_test, y_test = defense.fit(clean_pool, ds)
    
    # Evaluate Classifier Only on the test set
    preds_clf = defense.classifier.predict(X_test)
    report_clf = classification_report(y_test, preds_clf, output_dict=True)
    f1_benign_clf = report_clf['0']['f1-score']
    f1_malicious_clf = report_clf['1']['f1-score']
    macro_f1_clf = report_clf['macro avg']['f1-score']
    
    # To evaluate the Full Heuristic, we must re-encode texts because it requires the raw text and a mock query
    # We use the raw texts that correspond to X_test (we get them by re-splitting the dataframe exactly)
    df = ds.to_pandas()
    _, X_test_texts, _, y_test_labels = train_test_split(df['text'].tolist(), df['label'].tolist(), test_size=0.2, random_state=RANDOM_SEED, stratify=df['label'].tolist())
    
    # Simulated typical user query
    user_query = "What is the capital of France?"
    
    _, blocked_indices_heuristic = defense.filter_full_heuristic(user_query, X_test_texts)
    
    # Map blocked indices to predictions (blocked = 1, allowed = 0)
    preds_heur = [1 if i in blocked_indices_heuristic else 0 for i in range(len(X_test_texts))]
    
    report_heur = classification_report(y_test_labels, preds_heur, output_dict=True)
    f1_benign_heur = report_heur['0']['f1-score']
    f1_malicious_heur = report_heur['1']['f1-score']
    macro_f1_heur = report_heur['macro avg']['f1-score']
    
    results = [
        {
            "Variant": "Classifier Only",
            "Benign F1": f1_benign_clf,
            "Malicious F1": f1_malicious_clf,
            "Macro F1": macro_f1_clf
        },
        {
            "Variant": "Classifier + Goal-Redirection Heuristic",
            "Benign F1": f1_benign_heur,
            "Malicious F1": f1_malicious_heur,
            "Macro F1": macro_f1_heur
        }
    ]
    
    res_df = pd.DataFrame(results)
    res_df.to_csv(f"{OUTPUT_DIR}/results/security_ablation_metrics.csv", index=False)
    
    print("\n--- Security Ablation Results ---")
    print(res_df.to_string())

if __name__ == "__main__":
    main()
