import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score

# Paths
repo_root = Path(__file__).parent
submissions_dir = repo_root / "submissions"
labels_file = repo_root / "data" / "test_labels.csv"
leaderboard_file = repo_root / "leaderboard.csv"

def main():
    print("🏆 Running Leaderboard System...\n")

    # Load true labels
    if not labels_file.exists():
        print("❌ test_labels.csv not found")
        return

    y_true = pd.read_csv(labels_file)["Marine Heatwave"]

    results = []

    # Loop through submissions
    for file in submissions_dir.glob("*.csv"):
        print(f"Processing {file.name}")

        try:
            df = pd.read_csv(file)

            if "prediction" not in df.columns:
                print(f"⚠️ Skipping {file.name} (no prediction column)")
                continue

            y_pred = df["prediction"]

            # Calculate accuracy
            acc = accuracy_score(y_true, y_pred)

            results.append({
                "team_name": file.stem,
                "accuracy": round(acc * 100, 2)
            })

        except Exception as e:
            print(f"❌ Error in {file.name}: {e}")

    # Create leaderboard
    leaderboard = pd.DataFrame(results)

    if leaderboard.empty:
        print("No valid submissions found")
        return

    # Sort by accuracy
    leaderboard = leaderboard.sort_values(by="accuracy", ascending=False)
    leaderboard.insert(0, "rank", range(1, len(leaderboard) + 1))

    # Save leaderboard
    leaderboard.to_csv(leaderboard_file, index=False)

    print("\n🏆 Leaderboard Updated!\n")
    print(leaderboard.to_string(index=False))


if __name__ == "__main__":
    main()
