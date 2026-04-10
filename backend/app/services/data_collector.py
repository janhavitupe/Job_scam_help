import csv
import os

DATA_PATH = "ml/collected_data.csv"

def log_email(text, label=None):
    file_exists = os.path.isfile(DATA_PATH)

    with open(DATA_PATH, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["text", "label"])

        writer.writerow([text, label if label is not None else ""])