import json
import os

# Step 1: Get username from GitHub
username = os.getenv("GITHUB_ACTOR", "unknown_user")

# Step 2: For now we use dummy accuracy (we will fix later)
accuracy = 0.85  

# Step 3: Save result
result = {
    "name": username,
    "accuracy": accuracy
}

with open("result.json", "w") as f:
    json.dump(result, f)

print("Result saved:", result)
