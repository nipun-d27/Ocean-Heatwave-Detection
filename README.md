# 🌊 AI-Based Marine Heatwave Detection & Prediction System

## 📌 Project Overview
This project focuses on detecting and predicting marine heatwaves using machine learning techniques. The system uses environmental and geographical parameters to classify whether a marine heatwave condition is present or not.

We use a **Random Forest Classifier** to perform classification based on oceanographic and climatic features.

---

## 🎯 Objective
To build an AI model that can:
- Detect marine heatwave conditions
- Predict future occurrences based on environmental features
- Assist in climate monitoring and marine ecosystem protection

---

## 📊 Dataset Features (X)

The input features used for training the model:

- 🌡️ pH Level of water  
- 📍 Latitude  
- 📍 Longitude  
- 📅 Month (seasonal variation)

---

## 🎯 Target Variable (Y)

- 🌊 Heatwave Label  
  - `1` → Marine Heatwave Present  
  - `0` → No Marine Heatwave  

---

## 🤖 Machine Learning Model

- Algorithm Used: **Random Forest Classifier**
- Reason:
  - Handles non-linear relationships well  
  - Reduces overfitting using multiple decision trees  
  - Works well with structured environmental data  

---

## ⚙️ Workflow

1. Data collection and preprocessing  
2. Feature selection (pH, latitude, longitude, month)  
3. Train-test split  
4. Model training using Random Forest  
5. Prediction of marine heatwave condition  
6. Performance evaluation  

---

## 🧪 Libraries Used

- Python  
- Pandas  
- NumPy  
- Scikit-learn  
- Matplotlib / Seaborn (for visualization)

---

## 📈 Model Output

The model predicts:
- Whether a marine heatwave will occur (`1`)  
- Or not (`0`)

---

## 🚀 How to Run

```bash id="v9k3qa"
pip install -r requirements.txt
