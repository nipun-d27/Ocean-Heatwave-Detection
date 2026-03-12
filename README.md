# GTA (Graph Topology Ablation) Challenge

This repository hosts the official evaluation system for the **Graph Topology Ablation (GTA) challenge**. Participants submit predictions for ideal and perturbed graph topologies. All submissions are encrypted, automatically evaluated, and ranked on a public leaderboard.

📊 **Live leaderboard**: [Open leaderboard](https://idrees11.github.io/GTA-Graph-Topology-Ablation_-GTA-/)

---

## 🎯 Objective

Participants must generate predictions for two settings:

- ✅ **Ideal graph topology** – clean, unmodified node features.
- ✅ **Perturbed graph topology** – node features corrupted by a combination of distribution shift and Gaussian noise.

The goal is to build a Graph Neural Network (GNN) that is both accurate on clean data and robust to realistic feature corruptions.

---

## 📌 Dataset Description

We use the **MUTAG dataset**, a classic benchmark for graph classification from chemical informatics.

**🔗 Official source**:  
[https://ls11-www.cs.tu-dortmund.de/people/morris/graphkerneldatasets/MUTAG.zip](https://ls11-www.cs.tu-dortmund.de/people/morris/graphkerneldatasets/MUTAG.zip)

### Core Statistics

| Property                | Value                                    |
|-------------------------|------------------------------------------|
| Task                    | Binary graph classification              |
| Domain                  | Chemical compounds (mutagenic vs non‑mutagenic) |
| Number of graphs        | 188                                      |
| Avg. nodes per graph    | ~18                                      |
| Avg. edges per graph    | ~40                                      |
| Node features           | Categorical atom labels (interpreted as features) |
| Number of classes       | 2                                        |

Each graph represents a molecule:
- **Nodes** – atoms
- **Edges** – chemical bonds
- **Graph label** – indicates whether the molecule is mutagenic to *Salmonella typhimurium*.

### Data Split

The dataset is split **70/30** with stratification by class:

- `data/train.csv` – labeled training graphs (70%)
- `data/test.csv`  – unlabeled test graphs (30%)

Training labels are provided in `data/train.csv` with columns `graph_index` and `label`.  
Test graphs are listed in `data/test.csv` with only `graph_index` (labels are hidden for scoring).

---

## ⚙️ Perturbation Mechanism

Two types of feature corruption are applied to the test graphs to generate the **perturbed** setting:

1. **Distribution Shift**  
   A constant offset is added to each node feature:  
   `x ← x + δ`  
   where `δ = feature_shift` (default `0.3`).  
   *Simulates systematic measurement bias or domain shift.*

2. **Gaussian Noise Injection**  
   Random noise is added to each feature:  
   `x ← x + ϵ,  ϵ ~ N(0, σ²)`  
   where `σ = noise_std` (default `0.05`).  
   *Simulates noisy feature extraction.*

**Purpose**:  
This setup evaluates whether a GNN:
- relies on exact feature values,
- generalizes under feature distribution shift,
- remains stable under noisy topological descriptors.

The model is trained on clean features and evaluated on corrupted features to measure robustness.

---

## 📊 Evaluation Metrics

Performance is measured using the **F1 score** (macro‑averaged) because it balances precision and recall, providing a more reliable measure than accuracy alone.

Each submission is evaluated under two conditions:

- **F1 Score (Ideal)** – performance on clean topological features.
- **F1 Score (Perturbed)** – performance on corrupted features.

To quantify robustness, we compute the **Robustness Gap**:

`Robustness Gap = F1_ideal − F1_perturbed`

A smaller gap indicates a more stable and reliable model.

### 🏁 Ranking Priority

1. **Highest Perturbed F1 Score** (primary)
2. **Lowest Robustness Gap** (secondary)
3. **Most recent submission** (tie‑breaker)

Only the **best perturbed score** per participant is kept in the leaderboard.


-----------------------
## 🚀 Getting Started
-----------------------
 
### Environment Setup

Create a Python virtual environment and install dependencies:

```
Starter Code
A baseline GIN model is provided in starter_code/baseline.py. You can modify it or build your own model. 
```
The script Loads the MUTAG dataset:

```
Reads train.csv and test.csv.

Trains on clean graphs.

Generates predictions for both ideal and perturbed test graphs.

Saves submission files in the required format.
```
---------------------
To run the baseline:
---------------------
```
cd starter_code
starter_code/python baseline.py
```

This will create ideal_submission.csv and perturbed_submission.csv in the submissions/ folder (which is git‑ignored).

-------------------------
📤 Submission Procedure
-------------------------

Submissions must be encrypted and placed inside a folder named after your team.

**Step 1:** Prepare your submission files

Your CSV files must have the following format (example for 38 test graphs):

```
graph_index,label
160,1
62,0
48,0
173,1
.....
.....

ideal_submission.csv- predictions on clean test graphs.

perturbed_submission.csv – predictions on perturbed test graphs.
```

**Step 2:** Encrypt your files

From the project root, run the encryption script:

```
cd submissions
submissions/python encrypt_submissions.py
cd ..
```
This script will:

Look for ideal_submission.csv and perturbed_submission.csv in 'submissions' folder.

1.   Encrypt them using the public key (submissions/python encrypt_submissions.py).

2.   It will Produce ideal.enc and perturbed.enc in the same folder (submissions/<Team_Name>/*.enc).

Only the .enc files should be committed; the raw .csv files remain local (they are git‑ignored).
Note: Please dont forget to create submisions/<Team_Name>/  (two *enc files will be placed here)

**Step 3:** Commit and push

1.   Fork the repository.

2.   Create a folder submissions/<YourTeamName>/ and place the .enc files inside.
```
project_root/
├── encryption/
│   ├── __init__.py
│   └── encrypt.py           # contains encrypt_file function
├── submissions/
│   ├── sample_submission.csv
│   ├── file1.csv
│   ├── file2.csv
│   └── team_name/           # <-- folder created by script
│       ├── file1.csv.enc
│       └── file2.csv.enc
└── encrypt_submissions.py   # script that encrypts files
```

4.   Create a new branch, commit only the .enc files, and open a Pull Request (PR) against the main branch.


**Important:**

Do not commit any raw .csv files.

Ensure your team folder name does not contain spaces.

**Step 4:** Automatic evaluation

1.   Once the PR is opened, the automated workflow will:

2.   Decrypt your files (using the organiser’s private key, stored as a secret).

3.   Compute F1 scores for both ideal and perturbed submissions.

4.   Calculate the robustness gap.

5.   Update the leaderboard (only your best perturbed score is retained).

6.   The live leaderboard will reflect the new results within minutes.

--------------------------
📁 Repository Structure
--------------------------
```
gnn-topology-ablation/
│
├── .github/                       # GitHub Actions workflows
│   ├── scripts/                   # Helper scripts for evaluation
│   └── workflows/                 # CI/CD pipeline definition
│
├── data/                          # Dataset files
│   └── MUTAG/
│       ├── test.csv               # Test graph indices
│       └── train.csv              # Training labels
│
├── docs/                          # Live leaderboard website
│   ├── index.html
│   ├── leaderboard.css
│   ├── leaderboard.csv            # Auto‑generated ranking
│   ├── leaderboard.js
│   └── readme
│
├── encryption/                    # Encryption/decryption utilities
│   ├── __init__.py
│   ├── decrypt.py
│   ├── encrypt.py
│   ├── generate_keys.py
│   └── public_key.pem             # Public key for participants
│
├── leaderboard/                   # Scoring and ranking logic
│   ├── __init__.py
│   ├── calculate_scores.py
│   ├── hidden_labels_reader.py
│   ├── render_leaderboard.py
│   ├── score_submission.py
│   └── update_leaderboard.py
│
├── starter_code/                   # Participant starter kit
│   ├── baseline.py
│   └── requirements.txt
│
├── submissions/                    # Encrypted submissions (git‑tracked)
│   └──<Team_Name>
│   └── encrypt_submissions.py      # encrypts the *.CSVs
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── leaderboard.md
└── requirements.txt
└── scoring_scripts.py
└── utils.py
```

-----------------------
🔒 Security Guarantee
-----------------------

1.   Predictions are encrypted locally using a symmetric key, which is then encrypted with the organiser’s RSA public key.

2.   Only the organiser (with the corresponding private key stored as a GitHub secret) can decrypt the submissions.

3.   Encrypted files are visible in the repository but completely unreadable without the private key.

4.   This ensures blind evaluation – participants cannot see each other’s predictions, and the organiser cannot see them until after the submission
     deadline (if desired).
     
-------------
📜 License
------------
This project is released under the MIT License. See the LICENSE file for details.


