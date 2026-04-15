# .github/scripts/process_submission.py

from pathlib import Path
import sys
import os
import pandas as pd
import joblib  # for loading model

repo_root = Path(__file__).parent.parent.parent.resolve()

def main():
    submissions_dir = repo_root / "submissions"
    model_path = repo_root / "model" / "model.pkl"
    output_dir = repo_root / "predictions"

    print(f"DEBUG: Submissions directory: {submissions_dir}")

    if not submissions_dir.exists():
        print("No submissions directory found")
        return

    # Create output folder
    output_dir.mkdir(exist_ok=True)

    # Load trained Random Forest model
    print("Loading model...")
    model = joblib.load(model_path)

    print("Processing submissions...")

    for file in submissions_dir.glob("*.csv"):
        print(f"Processing {file.name}")

        # Load submission data
        df = pd.read_csv(file)

        # Features used in your model
        X = df[["ph", "latitude", "longitude", "month"]]

        # Predict
        predictions = model.predict(X)

        # Save predictions
        output_file = output_dir / f"{file.stem}_predictions.csv"
        df["prediction"] = predictions
        df.to_csv(output_file, index=False)

        print(f"Saved predictions to {output_file}")

    print("Processing complete!")


if __name__ == "__main__":
    main()
