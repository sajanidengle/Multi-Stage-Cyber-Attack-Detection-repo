import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, roc_auc_score
from sklearn.preprocessing import LabelEncoder, label_binarize
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
import seaborn as sns
import os
import joblib

print("Loading dataset...")

file_path = "data/final_ckc_dataset.csv"

df = pd.read_csv(file_path)

print("Total rows:", len(df))

# --------------------------------------------------
# STRATIFIED SAMPLING (2 MILLION ROWS)
# --------------------------------------------------

sample_size = 2_000_000

print("Performing stratified sampling...")

class_counts = df["CKC_Stage"].value_counts()

df_sampled_list = []

for stage in class_counts.index:
    
    stage_df = df[df["CKC_Stage"] == stage]
    
    stage_sample_size = int(sample_size * len(stage_df) / len(df))
    
    sampled_stage = stage_df.sample(
        n=stage_sample_size,
        random_state=42
    )
    
    df_sampled_list.append(sampled_stage)

df_sampled = pd.concat(df_sampled_list)

df_sampled = df_sampled.reset_index(drop=True)

print("Sampled rows:", len(df_sampled))

# --------------------------------------------------
# FEATURE / TARGET SPLIT
# --------------------------------------------------

X = df_sampled.drop(columns=["CKC_Stage", "Label"])
y = df_sampled["CKC_Stage"]

# --------------------------------------------------
# ENCODE TARGET LABELS
# --------------------------------------------------

le = LabelEncoder()

y_encoded = le.fit_transform(y)

# --------------------------------------------------
# TRAIN TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# --------------------------------------------------
# RANDOM FOREST MODEL
# --------------------------------------------------

print("Training Random Forest...")

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

rf.fit(X_train, y_train)

print("Model trained successfully.")

# --------------------------------------------------
# PREDICTIONS
# --------------------------------------------------

y_pred = rf.predict(X_test)

# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=le.classes_
    )
)

print("\nConfusion Matrix:\n")

print(confusion_matrix(y_test, y_pred))

# --------------------------------------------------
# FEATURE IMPORTANCE
# --------------------------------------------------

print("\nTop 20 Important Features:\n")

importances = rf.feature_importances_

feature_names = X.columns

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print(importance_df.head(20))

# --------------------------------------------------
# VISUALIZATIONS AND MODEL SAVING
# --------------------------------------------------

# Create outputs folder if not exists
os.makedirs("outputs", exist_ok=True)
os.makedirs("models", exist_ok=True)

# 1. CONFUSION MATRIX VISUALIZATION
print("\nGenerating Confusion Matrix...")

cm = confusion_matrix(y_test, y_pred)

# Enhanced confusion matrix plot
fig, ax = plt.subplots(figsize=(12, 10))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
disp.plot(cmap='Blues', ax=ax, xticks_rotation=45, values_format='d')

plt.title("Confusion Matrix - CKC Stage Classification", fontsize=16, fontweight='bold')
plt.xlabel("Predicted Label", fontsize=12)
plt.ylabel("True Label", fontsize=12)
plt.tight_layout()
plt.savefig("outputs/confusion_matrix.png", dpi=300, bbox_inches='tight')
print("Confusion matrix saved to outputs/confusion_matrix.png")
plt.close()

# 2. ROC CURVE VISUALIZATION (One-vs-Rest for multiclass)
print("Generating ROC Curves...")

# Get probability predictions for ROC curve
y_pred_proba = rf.predict_proba(X_test)

# Binarize the output for one-vs-rest approach
y_test_binarized = label_binarize(y_test, classes=np.arange(len(le.classes_)))

n_classes = len(le.classes_)
fpr = dict()
tpr = dict()
roc_auc = dict()

# Compute ROC curve and AUC for each class
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test_binarized[:, i], y_pred_proba[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and AUC
fpr_micro, tpr_micro, _ = roc_curve(y_test_binarized.ravel(), y_pred_proba.ravel())
roc_auc_micro = auc(fpr_micro, tpr_micro)

# Plot ROC curves
fig, ax = plt.subplots(figsize=(12, 10))
colors = plt.cm.tab20(np.linspace(0, 1, n_classes))

# Plot ROC curve for each class
for i, color in zip(range(n_classes), colors):
    ax.plot(
        fpr[i], tpr[i],
        color=color,
        lw=2.5,
        label=f'{le.classes_[i]} (AUC = {roc_auc[i]:.2f})'
    )

# Plot micro-average ROC curve
ax.plot(
    fpr_micro, tpr_micro,
    color='deeppink',
    linestyle='--',
    lw=3,
    label=f'Micro-average (AUC = {roc_auc_micro:.2f})'
)

# Plot diagonal line
ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')

ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('False Positive Rate', fontsize=12)
ax.set_ylabel('True Positive Rate', fontsize=12)
ax.set_title('ROC Curves - CKC Stage Classification (One-vs-Rest)', fontsize=16, fontweight='bold')
ax.legend(loc="lower right", fontsize=10)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/roc_curves.png", dpi=300, bbox_inches='tight')
print("ROC curves saved to outputs/roc_curves.png")
plt.close()

# 3. FEATURE IMPORTANCE VISUALIZATION
print("Generating Feature Importance plot...")

fig, ax = plt.subplots(figsize=(12, 10))
top_features = importance_df.head(20)
ax.barh(range(len(top_features)), top_features['Importance'].values, color='steelblue')
ax.set_yticks(range(len(top_features)))
ax.set_yticklabels(top_features['Feature'].values)
ax.set_xlabel('Importance Score', fontsize=12)
ax.set_ylabel('Features', fontsize=12)
ax.set_title('Top 20 Feature Importance - Random Forest CKC Stage Classifier', fontsize=16, fontweight='bold')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/feature_importance.png", dpi=300, bbox_inches='tight')
print("Feature importance plot saved to outputs/feature_importance.png")
plt.close()

# 4. SAVE MODEL
print("\nSaving trained model...")
joblib.dump(rf, "models/random_forest_ckc.pkl")
print("Model saved to models/random_forest_ckc.pkl")

print("\n" + "="*50)
print("All visualizations generated successfully!")
print("="*50)
print(f"\nAUC Scores by Class:")
for i, class_name in enumerate(le.classes_):
    print(f"  {class_name}: {roc_auc[i]:.4f}")
print(f"  Micro-average: {roc_auc_micro:.4f}")