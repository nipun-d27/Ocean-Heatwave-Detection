import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score

# ───────────────────────────────────────────────
# HANDLE PATH (works in Jupyter + script)
# ───────────────────────────────────────────────
try:
    repo_root = Path(__file__).parent
except NameError:
    repo_root = Path().resolve()

submissions_dir = repo_root / "submissions"
labels_file = repo_root / "data" / "test_labels.csv"
leaderboard_file = repo_root / "leaderboard.csv"

print(f"📂 Repo path: {repo_root}")

# ───────────────────────────────────────────────
# LOAD TRUE LABELS
# ───────────────────────────────────────────────
if not labels_file.exists():
    print("❌ test_labels.csv not found!")
    print(f"Expected at: {labels_file}")
    
    # Create empty leaderboard
    pd.DataFrame(columns=["rank", "team_name", "accuracy"]).to_csv(leaderboard_file, index=False)
    print("⚠️ Empty leaderboard.csv created")
    exit()

y_true = pd.read_csv(labels_file)["Marine Heatwave"]

# ───────────────────────────────────────────────
# PROCESS SUBMISSIONS
# ───────────────────────────────────────────────
results = []

if not submissions_dir.exists():
    print("⚠️ No submissions folder found")
    submissions_dir.mkdir(exist_ok=True)

files = list(submissions_dir.glob("*.csv"))

if not files:
    print("⚠️ No submission files found")

for file in files:
    print(f"📄 Processing: {file.name}")

    try:
        df = pd.read_csv(file)

        # Check column
        if "prediction" not in df.columns:
            print(f"⚠️ Skipping {file.name} (no 'prediction' column)")
            continue

        y_pred = df["prediction"]

        # Check length match
        if len(y_pred) != len(y_true):
            print(f"⚠️ Skipping {file.name} (length mismatch)")
            continue

        acc = accuracy_score(y_true, y_pred)

        results.append({
            "team_name": file.stem,
            "accuracy": round(acc * 100, 2)
        })

    except Exception as e:
        print(f"❌ Error in {file.name}: {e}")

# ───────────────────────────────────────────────
# CREATE LEADERBOARD
# ───────────────────────────────────────────────
if results:
    leaderboard = pd.DataFrame(results)
    leaderboard = leaderboard.sort_values(by="accuracy", ascending=False)
    leaderboard.insert(0, "rank", range(1, len(leaderboard) + 1))
else:
    print("⚠️ No valid submissions — creating empty leaderboard")
    leaderboard = pd.DataFrame(columns=["rank", "team_name", "accuracy"])

# ───────────────────────────────────────────────
# SAVE FILE
# ───────────────────────────────────────────────
leaderboard.to_csv(leaderboard_file, index=False)

print("\n🏆 Leaderboard created successfully!")
print(f"📁 Saved at: {leaderboard_file.resolve()}")

print("\n📊 Leaderboard Preview:")
print(leaderboard.to_string(index=False))
