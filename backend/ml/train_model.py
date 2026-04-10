import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Paths
BASE_PATH = os.path.dirname(__file__)
DATASET_PATH = os.path.join(BASE_PATH, "dataset.csv")
COLLECTED_PATH = os.path.join(BASE_PATH, "collected_data.csv")

# -------- Load datasets --------
df_list = []

if os.path.exists(DATASET_PATH):
    df1 = pd.read_csv(DATASET_PATH)
    df_list.append(df1)

if os.path.exists(COLLECTED_PATH):
    df2 = pd.read_csv(COLLECTED_PATH)
    df_list.append(df2)

df = pd.concat(df_list, ignore_index=True)

# -------- Clean data --------
df = df.dropna(subset=["text", "label"])   # remove empty labels
df["text"] = df["text"].astype(str)
df["label"] = df["label"].astype(int)

print("Dataset size:", len(df))

# -------- Vectorization --------
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=8000,
    ngram_range=(1, 2)
)


X = vectorizer.fit_transform(df["text"])
y = df["label"]

# -------- Train/Test Split --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------- Model --------
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)
model.fit(X_train, y_train)

# -------- Evaluation --------
y_pred = model.predict(X_test)
print("\nModel Performance:\n")
print(classification_report(y_test, y_pred))

# -------- Save --------
joblib.dump(model, os.path.join(BASE_PATH, "model.pkl"))
joblib.dump(vectorizer, os.path.join(BASE_PATH, "vectorizer.pkl"))

print("\nModel saved successfully.")