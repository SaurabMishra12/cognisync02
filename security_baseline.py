import os
import numpy as np
import pandas as pd
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

print("Loading dataset 'deepset/prompt-injections'...")
dataset = load_dataset('deepset/prompt-injections', split='train')
df = dataset.to_pandas()

# The dataset has 'text' and 'label'. Label 1 = injection, 0 = legitimate
texts = df['text'].tolist()
labels = df['label'].tolist()

print(f"Loaded {len(texts)} texts. {sum(labels)} injections, {len(labels)-sum(labels)} legitimate.")

# Split into train/test
texts_train, texts_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42, stratify=labels)

print("Loading SentenceTransformer...")
encoder = SentenceTransformer('all-MiniLM-L6-v2')

print("Encoding train set...")
X_train_embs = encoder.encode(texts_train, show_progress_bar=True)

# Separate clean docs from train to find centroid (mu)
clean_embs_train = X_train_embs[np.array(y_train) == 0]
mean_emb = np.mean(clean_embs_train, axis=0)
mu = mean_emb / (np.linalg.norm(mean_emb) + 1e-10)

IMPERATIVE_VERBS = ["ignore", "reveal", "execute", "forget", "bypass", "output"]
def has_imperative(text):
    text_lower = text.lower()
    return 1.0 if any(verb in text_lower for verb in IMPERATIVE_VERBS) else 0.0

avg_len_clean = np.mean([len(t) for t, y in zip(texts_train, y_train) if y == 0])

def extract_features(texts, embs):
    features = []
    for i, text in enumerate(texts):
        emb = embs[i]
        cos_sim = np.dot(emb / (np.linalg.norm(emb) + 1e-10), mu)
        imp = has_imperative(text)
        len_ratio = len(text) / avg_len_clean
        features.append([cos_sim, imp, len_ratio])
    return np.array(features)

print("Extracting training features...")
X_train_features = extract_features(texts_train, X_train_embs)

print("Training Logistic Classifier...")
classifier = LogisticRegression(class_weight='balanced')
classifier.fit(X_train_features, y_train)

print("Encoding test set...")
X_test_embs = encoder.encode(texts_test, show_progress_bar=True)
X_test_features = extract_features(texts_test, X_test_embs)

print("Evaluating...")
y_pred = classifier.predict(X_test_features)
y_prob = classifier.predict_proba(X_test_features)[:, 1]

# Heuristic: if imperative and low similarity to typical query
# We don't have typical queries here, but we can simulate the second gate if needed.
# For now, we just evaluate the classifier's performance.

# Calculate FPR and ASR (Attack Success Rate = False Negative Rate)
# Positive class (1) = Adversarial (Attack)
# Negative class (0) = Legitimate
# FP = Predicted 1, Actual 0 (Legitimate blocked)
# FN = Predicted 0, Actual 1 (Attack succeeded)

fp = sum(1 for i in range(len(y_test)) if y_pred[i] == 1 and y_test[i] == 0)
tn = sum(1 for i in range(len(y_test)) if y_pred[i] == 0 and y_test[i] == 0)
fn = sum(1 for i in range(len(y_test)) if y_pred[i] == 0 and y_test[i] == 1)
tp = sum(1 for i in range(len(y_test)) if y_pred[i] == 1 and y_test[i] == 1)

fpr = fp / (fp + tn) if (fp+tn) > 0 else 0
asr = fn / (fn + tp) if (fn+tp) > 0 else 0

print(f"\n--- Deepset Prompt Injections Baseline Evaluation ---")
print(f"False Positive Rate (Legitimate Docs Blocked): {fpr:.4f} ({fpr*100:.2f}%)")
print(f"Attack Success Rate (Injections Evading Filter): {asr:.4f} ({asr*100:.2f}%)")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Injection"]))

with open("security_baseline_results.txt", "w") as f:
    f.write(f"FPR: {fpr:.4f}\nASR: {asr:.4f}\n")
