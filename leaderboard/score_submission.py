import os
from pathlib import Path
from leaderboard.calculate_scores import calculate_scores_pair


def score():
    """
    Score participant submissions and return leaderboard metrics.
    """

    submissions_dir = Path("submissions")

    ideal_path = submissions_dir / "ideal_submission.csv"
    perturbed_path = submissions_dir / "perturbed_submission.csv"

    if not ideal_path.exists():
        raise FileNotFoundError(f"{ideal_path} not found")

    if not perturbed_path.exists():
        raise FileNotFoundError(f"{perturbed_path} not found")

    scores = calculate_scores_pair(ideal_path, perturbed_path)

    print("Scores:", scores)

    return scores


if __name__ == "__main__":
    score()
