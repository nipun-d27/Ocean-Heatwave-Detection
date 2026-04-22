import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score

# ─────────────────────────────────────────────
# Set paths (works for GitHub + local)
# ─────────────────────────────────────────────
try:
    repo_root = Path(__file__).parent
except NameError:
    repo_root = Path().resolve()

submissions_dir = repo_root / "submissions"
labels_file = repo_root / "data" / "test_labels.csv"
leaderboard_file = repo_root / "leaderboard.csv"

print("📂 Project path:", repo_root)

# ─────────────────────────────────────────────
# Load ground truth labels
# ─────────────────────────────────────────────
if not labels_file.exists():
    print("❌ test_labels.csv not found at:", labels_file)
    exit()

y_true = pd.read_csv(labels_file)["Marine Heatwave"]

# ─────────────────────────────────────────────
# Process submissions
# ─────────────────────────────────────────────
results = []

if not submissions_dir.exists():
    print("⚠️ No submissions folder found")
    submissions_dir.mkdir()

files = list(submissions_dir.glob("*.csv"))

if len(files) == 0:
    print("⚠️ No submission files found in submissions/")
else:
    for file in files:
        print(f"📄 Processing {file.name}")

        df = pd.read_csv(file)

        if "prediction" not in df.columns:
            print(f"⚠️ Skipping {file.name} (no 'prediction' column)")
            continue

        y_pred = df["prediction"]

        if len(y_pred) != len(y_true):
            print(f"⚠️ Skipping {file.name} (row mismatch)")
            continue

        acc = accuracy_score(y_true, y_pred)

        results.append({
            "team_name": file.stem,
            "accuracy": round(acc * 100, 2)
        })

# ─────────────────────────────────────────────
# Create leaderboard
# ─────────────────────────────────────────────
if results:
    leaderboard = pd.DataFrame(results)
    leaderboard = leaderboard.sort_values(by="accuracy", ascending=False)
    leaderboard.insert(0, "rank", range(1, len(leaderboard) + 1))
else:
    leaderboard = pd.DataFrame(columns=["rank", "team_name", "accuracy"])

# ─────────────────────────────────────────────
# Save file
# ─────────────────────────────────────────────
leaderboard.to_csv(leaderboard_file, index=False)

print("\n🏆 Leaderboard created successfully!")
print("📁 Saved at:", leaderboard_file.resolve())

print("\n📊 Leaderboard Preview:")
print(leaderboard)
