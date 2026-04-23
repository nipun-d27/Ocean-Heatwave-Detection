# 🌊 Ocean Heatwave Detector (AI-Based System)

## 📌 Project Overview
This project implements an AI-based system to detect and predict marine heatwaves using oceanographic and environmental data. The model is built from scratch using the Delta Rule (Widrow-Hoff Learning Algorithm), a supervised learning approach that updates weights using gradient-based optimization.

---
## 🏆 Leaderboard

| Name | Accuracy |
|------|----------|

👉 [View Full Leaderboard](./leaderboard.csv)
---

## 🎯 Objective
- Detect marine heatwave conditions from ocean data  
- Understand environmental patterns affecting heatwaves  
- Build a machine learning model from scratch without relying on high-level APIs  

---

## 📊 Dataset

**File Used:** `realistic_ocean_climate_dataset.csv`

### Features:
- Location (encoded)
- Sea Surface Temperature (SST °C)
- pH Level
- Bleaching Severity
- Species Observed

### Dropped Features:
- Date  
- Latitude  
- Longitude  

### Target Variable:
- Marine Heatwave  
  - 1 → Heatwave present  
  - 0 → Normal condition  

---

## ⚙️ Workflow

### 1️⃣ Data Loading
- Load dataset using Pandas  
- Display structure, features, and class distribution  

### 2️⃣ Preprocessing
- Drop unnecessary columns (Date, Latitude, Longitude)  
- Encode categorical features:
  - Location → Label Encoding  
  - Bleaching Severity → Numerical mapping  
- Convert target variable to binary  
- Handle missing values  

---

### 3️⃣ Train-Test Split & Normalization
- Split dataset into 80% training and 20% testing using train_test_split  
- Apply StandardScaler for normalization  
- Add bias term manually to input features  

---

### 4️⃣ Exploratory Data Analysis (EDA)
- Distribution of SST for heatwave vs normal conditions  
- Class balance visualization  
- Scatter plot of pH vs SST  
- Heatwave rate vs bleaching severity  

Output:
- eda.png  

---

### 5️⃣ Model: Delta Rule Neuron

The model is implemented manually using the Delta Rule.

#### Algorithm:
- Weighted sum: z = W · x  
- Activation: sigmoid function  
- Error: δ = y − ŷ  
- Weight update:
  ΔW = η × δ × σ'(z) × x  

#### Features:
- Custom neural model implementation  
- No use of sklearn classifiers  
- Tracks loss and accuracy during training  

---

### 6️⃣ Evaluation

Metrics used:
- Accuracy  
- Precision  
- Recall  
- F1 Score  
- Confusion Matrix  

Also includes sklearn classification_report for detailed analysis  

---

### 7️⃣ Testing on New Data
- Create new unseen samples manually  
- Apply trained model  
- Output predicted probability and classification  

---

### 8️⃣ Visualization

Generated plots:
- Training loss curve  
- Training accuracy curve  
- Confusion matrix  
- Predictions on new samples  

Output:
- results.png  

---

## 🧠 Model Insights
- Higher SST and lower pH are strong indicators of heatwaves  
- Bleaching severity has a direct relationship with heatwave occurrence  
- The model learns non-linear relationships using sigmoid activation  

---

## 📦 Libraries Used
- NumPy  
- Pandas  
- Matplotlib  
- Scikit-learn  

---

## 🚀 How to Run

Install dependencies:
pip install numpy pandas matplotlib scikit-learn

Run the script:
python your_script_name.py  

---

## 📂 Outputs
- eda.png → Exploratory data analysis plots  
- results.png → Model performance and predictions  

---

## 🔥 Key Highlights
- Machine learning model built from scratch (Delta Rule)  
- End-to-end pipeline: preprocessing → training → evaluation  
- Real-world application in climate and marine monitoring  
- Strong visualizations and interpretability  

---

## 📌 Future Improvements
- Replace Delta Rule with Random Forest or Deep Learning models  
- Add time-series forecasting (LSTM)  
- Use real-time ocean datasets  
- Deploy as a web application or dashboard  

---

## 🌍 Impact
This system can help in:
- Climate change monitoring  
- Marine ecosystem protection  
- Early detection of marine heatwaves  

---

## 👨‍💻 Author
Developed as a Data Science project focusing on AI applications in environmental systems.
