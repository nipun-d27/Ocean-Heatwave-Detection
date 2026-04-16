import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                                     confusion_matrix, classification_report)

df=pd.read_csv('/content/Ocean Heatwave Data.zip')
df.head()

print("STEP 1: DATA OVERVIEW")
print(f"  Rows       : {df.shape[0]}")
print(f"  Columns    : {df.shape[1]}")
print(f"  Features   : {df.columns.tolist()}")
print(f"\n  First 3 rows:")
print(df.head(3).to_string())
print(f"\n  Heatwave counts:\n{df['Marine Heatwave'].value_counts()}")

print("STEP 2: PREPROCESSING")
df = df.drop(columns=['Date', 'Latitude', 'Longitude'])
print(f"  Dropped: Date, Latitude, Longitude")

le_location = LabelEncoder()
df['Location'] = le_location.fit_transform(df['Location'])
print(f"  Encoded Location: {dict(zip(le_location.classes_, le_location.transform(le_location.classes_)))}")

bleach_map = {'None': 0, 'Low': 1, 'Medium': 2, 'High': 3}
df['Bleaching Severity'] = df['Bleaching Severity'].fillna('None')
df['Bleaching Severity'] = df['Bleaching Severity'].map(bleach_map)
print(f"  Encoded Bleaching Severity: {bleach_map}")

df['Marine Heatwave'] = df['Marine Heatwave'].astype(int)
print(f"\n  Target distribution after encoding:")
print(f"  {df['Marine Heatwave'].value_counts().to_dict()}")

print(f"\n  Null values after cleaning:")
print(f"  {df.isnull().sum().to_dict()}")
print(f"\n  Final dataset shape: {df.shape}")
print(f"  Columns used: {df.columns.tolist()}")

print("STEP 3: TRAIN/TEST SPLIT + NORMALIZATION")

X = df.drop(columns=['Marine Heatwave']).values.astype(np.float32)
y = df['Marine Heatwave'].values.astype(np.float32)

feature_names = df.drop(columns=['Marine Heatwave']).columns.tolist()
print(f"  Feature matrix shape : {X.shape}")
print(f"  Target vector shape  : {y.shape}")
print(f"  Features             : {feature_names}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size    = 0.2,
    random_state = 42,
    stratify     = y
)
print(f"\n  train_test_split (sklearn):")
print(f"  Training samples : {X_train.shape[0]}")
print(f"  Test samples     : {X_test.shape[0]}")
print(f"  Train heatwaves  : {int(y_train.sum())} / {len(y_train)}")
print(f"  Test  heatwaves  : {int(y_test.sum())}  / {len(y_test)}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit + transform
X_test_scaled = scaler.transform(X_test)        # transform only

print(f"\n  StandardScaler (sklearn):")
print(f"  Fitted on training set only (no data leakage)")
print(f"  Train mean after scaling : {X_train_scaled.mean():.4f}  (should be ≈ 0)")
print(f"  Train std  after scaling : {X_train_scaled.std():.4f}   (should be ≈ 1)")

X_train_b = np.hstack([X_train_scaled, np.ones((X_train_scaled.shape[0], 1))])
X_test_b  = np.hstack([X_test_scaled,  np.ones((X_test_scaled.shape[0],  1))])
print(f"\n  Bias column added.")
print(f"  Final input size: {X_train_b.shape[1]}  ({len(feature_names)} features + 1 bias)")

print("  STEP 4: EXPLORATORY DATA ANALYSIS")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("EDA — Ocean Heatwave Dataset", fontsize=14, fontweight='bold')
# Plot 1: SST distribution by class
ax = axes[0, 0]
sst_hw  = df[df['Marine Heatwave'] == 1]['SST (°C)']
sst_nor = df[df['Marine Heatwave'] == 0]['SST (°C)']
ax.hist(sst_nor, bins=20, color='#378ADD', alpha=0.7, label='Normal',   density=True)
ax.hist(sst_hw,  bins=20, color='#E24B4A', alpha=0.7, label='Heatwave', density=True)
ax.set_title("SST Distribution by Class")
ax.set_xlabel("SST (°C)")
ax.set_ylabel("Density")
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: Class balance bar chart
ax = axes[0, 1]
counts = df['Marine Heatwave'].value_counts()
ax.bar(['Normal (0)', 'Heatwave (1)'], counts.values,
       color=['#378ADD', '#E24B4A'], alpha=0.85, width=0.5)
for i, v in enumerate(counts.values):
    ax.text(i, v + 3, str(v), ha='center', fontweight='bold')
ax.set_title("Class Balance")
ax.set_ylabel("Count")
ax.grid(True, axis='y', alpha=0.3)

# Plot 3: pH Level vs SST (scatter, colored by label)
ax = axes[1, 0]
ax.scatter(df[df['Marine Heatwave']==0]['pH Level'],
           df[df['Marine Heatwave']==0]['SST (°C)'],
           color='#378ADD', s=20, alpha=0.6, label='Normal')
ax.scatter(df[df['Marine Heatwave']==1]['pH Level'],
           df[df['Marine Heatwave']==1]['SST (°C)'],
           color='#E24B4A', s=40, alpha=0.8, label='Heatwave')
ax.set_title("pH Level vs SST")
ax.set_xlabel("pH Level")
ax.set_ylabel("SST (°C)")
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 4: Bleaching Severity vs Heatwave
ax = axes[1, 1]
bleach_hw = df.groupby('Bleaching Severity')['Marine Heatwave'].mean() * 100
ax.bar(bleach_hw.index, bleach_hw.values,
       color=['#1D9E75','#FAC775','#E85D24','#E24B4A'], alpha=0.85)
ax.set_title("Heatwave Rate by Bleaching Severity")
ax.set_xlabel("Bleaching Severity (0=None, 1=Low, 2=Med, 3=High)")
ax.set_ylabel("Heatwave rate (%)")
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("eda.png", dpi=150, bbox_inches='tight')
plt.show()
print("  Saved → eda.png")

print("  STEP 5: DELTA RULE (WIDROW-HOFF)")

print("""
  THE DELTA RULE:
  ───────────────
  Forward pass:
      z  = W · x          (weighted sum)
      ŷ  = σ(z)           (sigmoid: output ∈ [0,1])

  Error:
      δ  = y − ŷ          (how wrong we are)

  Weight update:
      ΔW = η × δ × σ'(z) × x
      W  ← W + ΔW
  where σ'(z) = ŷ × (1 − ŷ)
""")

class DeltaRuleNeuron:

    def __init__(self, n_inputs, lr=0.05):
        # Small random initial weights
        self.W          = np.random.randn(n_inputs) * 0.01
        self.lr         = lr
        self.loss_hist  = []
        self.acc_hist   = []

    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

    def predict_proba(self, X):
        return self.sigmoid(X @ self.W)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)

    def train(self, X, y, epochs=300):
        n = X.shape[0]
        print(f"  Training for {epochs} epochs on {n} samples...")
        print(f"  {'─'*40}")

        for epoch in range(epochs):

            # ── Forward pass ──────────────────────────────
            yhat  = self.predict_proba(X)           # predicted probability

            # ── Compute error ─────────────────────────────
            error = y - yhat                         # δ = target − predicted

            # ── Sigmoid derivative ────────────────────────
            sig_d = yhat * (1 - yhat)               # σ'(z)

            # ── DELTA RULE: update weights ─────────────────
            # ΔW = η × (1/n) × Xᵀ × (error × σ'(z))
            self.W += self.lr * (X.T @ (error * sig_d)) / n

            # ── Track metrics ─────────────────────────────
            loss = np.mean((y - yhat) ** 2)         # MSE loss
            acc  = accuracy_score(y, self.predict(X))
            self.loss_hist.append(loss)
            self.acc_hist.append(acc)

            if (epoch + 1) % 50 == 0 or epoch == 0:
                print(f"  Epoch {epoch+1:3d}/{epochs}  "
                      f"loss={loss:.5f}  acc={acc*100:.1f}%")

        print(f"  {'─'*40}")
        print(f"  Training complete!")

np.random.seed(42)
neuron = DeltaRuleNeuron(n_inputs=X_train_b.shape[1], lr=0.1)
neuron.train(X_train_b, y_train, epochs=300)

print("  STEP 6: EVALUATION ON TEST SET")

y_pred      = neuron.predict(X_test_b)
y_pred_prob = neuron.predict_proba(X_test_b)

print(f"\n  sklearn classification_report:")
print(classification_report(y_test, y_pred,
                             target_names=['Normal', 'Heatwave'],
                             zero_division=0))

print(f"  accuracy_score  : {accuracy_score(y_test,  y_pred)*100:.2f}%")
print(f"  precision_score : {precision_score(y_test, y_pred, zero_division=0)*100:.2f}%")
print(f"  recall_score    : {recall_score(y_test,    y_pred, zero_division=0)*100:.2f}%")
print(f"  f1_score        : {f1_score(y_test,        y_pred, zero_division=0):.4f}")

cm = confusion_matrix(y_test, y_pred)
print(f"\n  confusion_matrix (sklearn):")
print(f"  [[TN={cm[0,0]}  FP={cm[0,1]}]")
print(f"   [FN={cm[1,0]}  TP={cm[1,1]}]]")

print("  STEP 7: TESTING ON NEW FEATURES")

print("""
  We create 5 brand-new sample observations not from
  the dataset and see what the trained neuron predicts.

  Features order: Location, SST(°C), pH, Bleaching, Species
""")

# New observations — manually crafted
# Location encoding: Great Barrier Reef=1, Red Sea=5, Maldives=3
# Bleaching: None=0, Low=1, Medium=2, High=3

new_samples = pd.DataFrame({
    'Location'          : [1, 5, 3, 0, 6],        # GBR, Red Sea, Maldives, Caribbean, SCS
    'SST (°C)'          : [33.0, 31.5, 29.0, 25.0, 32.8],
    'pH Level'          : [7.90, 7.95, 8.05, 8.10, 7.88],
    'Bleaching Severity': [3,    3,    1,    0,    3   ],
    'Species Observed'  : [60,   75,   115,  140,  65  ],
})

labels_desc = [
    "Very hot GBR, high bleaching",
    "Hot Red Sea, high bleaching",
    "Warm Maldives, low bleaching",
    "Cool Caribbean, no bleaching",
    "Very hot S. China Sea, high bleaching",
]

print(f"  New samples:\n{new_samples.to_string()}\n")

X_new        = new_samples.values.astype(np.float32)
X_new_scaled = scaler.transform(X_new)              # use already fitted scaler
X_new_b      = np.hstack([X_new_scaled,
                           np.ones((X_new_scaled.shape[0], 1))])

new_probs  = neuron.predict_proba(X_new_b)
new_preds  = neuron.predict(X_new_b)

print(f"  {'#':<4} {'Description':<40} {'Prob':>6}  {'Prediction'}")
print(f"  {'─'*4}  {'─'*40}  {'─'*6}  {'─'*15}")
for i in range(len(new_samples)):
    label = "HEATWAVE" if new_preds[i] == 1 else "Normal"
    print(f"  {i+1:<4} {labels_desc[i]:<40} {new_probs[i]:.4f}  {label}")

print("STEP 8: RESULTS VISUALIZATION")
fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle("Delta Rule — Training & Results", fontsize=14, fontweight='bold')

# Plot 1: Loss curve
ax = axes2[0, 0]
ax.plot(neuron.loss_hist, color='#E24B4A', lw=1.5)
ax.set_title("Training Loss (MSE)")
ax.set_xlabel("Epoch")
ax.set_ylabel("MSE Loss")
ax.grid(True, alpha=0.3)

# Plot 2: Accuracy curve
ax = axes2[0, 1]
ax.plot([a*100 for a in neuron.acc_hist], color='#1D9E75', lw=1.5)
ax.set_title("Training Accuracy")
ax.set_xlabel("Epoch")
ax.set_ylabel("Accuracy (%)")
ax.set_ylim(0, 105)
ax.grid(True, alpha=0.3)

# Plot 3: Confusion matrix
ax = axes2[1, 0]
im = ax.imshow(cm, cmap='Blues')
plt.colorbar(im, ax=ax)
for i in range(2):
    for j in range(2):
        ax.text(j, i, str(cm[i, j]), ha='center', va='center',
                fontsize=18, fontweight='bold',
                color='white' if cm[i,j] > cm.max()/2 else 'black')
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Pred: Normal', 'Pred: Heatwave'])
ax.set_yticklabels(['Act: Normal',  'Act: Heatwave'])
ax.set_title("Confusion Matrix (Test Set)")

# Plot 4: New sample predictions
ax = axes2[1, 1]
colors = ['#E24B4A' if p == 1 else '#378ADD' for p in new_preds]
bars   = ax.barh(range(len(new_samples)), new_probs,
                 color=colors, alpha=0.85)
ax.axvline(0.5, color='black', lw=1.5, ls='--', label='Threshold = 0.5')
ax.set_yticks(range(len(new_samples)))
ax.set_yticklabels([f"Sample {i+1}" for i in range(len(new_samples))], fontsize=9)
ax.set_xlabel("Predicted probability")
ax.set_title("New Sample Predictions")
ax.set_xlim(0, 1.1)
ax.legend()
ax.grid(True, axis='x', alpha=0.3)
for i, (prob, pred) in enumerate(zip(new_probs, new_preds)):
    label = "HEATWAVE" if pred == 1 else "Normal"
    ax.text(prob + 0.02, i, label, va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig("results.png", dpi=150, bbox_inches='tight')
plt.show()
print("\n  Saved → results.png")

# ── Final summary ─────────────────────────────────────
print("\n" + "=" * 50)
print("  DONE! Files saved:")
print("    eda.png      — exploratory analysis")
print("    results.png  — training curves + predictions")
print("=" * 50)
