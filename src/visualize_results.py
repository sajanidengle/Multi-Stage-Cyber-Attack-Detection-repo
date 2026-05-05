import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import joblib

# Create output folder
os.makedirs("outputs", exist_ok=True)

print("Loading model and data...")

# Load model (if saved earlier)
model = joblib.load("models/random_forest_ckc.pkl")

# Load dataset
df = pd.read_csv("data/final_ckc_dataset.csv")

# Prepare data
X = df.drop(columns=["CKC_Stage", "Label"])
y = df["CKC_Stage"]

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Predict
y_pred = model.predict(X)

# --------------------------------------------------
# CONFUSION MATRIX
# --------------------------------------------------

cm = confusion_matrix(y_encoded, y_pred)

plt.figure(figsize=(12, 10))

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=le.classes_,
    yticklabels=le.classes_
)

plt.title("Confusion Matrix - CKC Stage Classification")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.xticks(rotation=45)
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig("outputs/confusion_matrix.png", dpi=300)

plt.show()

# --------------------------------------------------
# FEATURE IMPORTANCE
# --------------------------------------------------

importances = model.feature_importances_
feature_names = X.columns

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False).head(20)

plt.figure(figsize=(10, 8))

plt.barh(importance_df["Feature"], importance_df["Importance"])

plt.gca().invert_yaxis()

plt.title("Top 20 Important Features")

plt.tight_layout()
plt.savefig("outputs/feature_importance.png", dpi=300)

plt.show()

print("Visualizations saved in outputs/")