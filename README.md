# 🏠 Airbnb Price Prediction Using Machine Learning

This project focuses on building a regression model to **predict Airbnb listing prices** based on various property and host attributes. The goal is to provide actionable insights for hosts and improve Airbnb's pricing strategy.

---

## 📦 Dataset Overview

- **Total Listings:** 74,111
- **Features:** Property type, location, room type, reviews, amenities, etc.
- **Target Variable:** `log_price` (log-transformed price)

---

## 🎯 Project Objectives

- Build a machine learning model to predict listing prices
- Handle missing values and outliers effectively
- Engineer features such as amenity count and host activity
- Evaluate model performance using RMSE, MAE, and R²
- Provide feature importance for interpretability

---

## 🔍 Key Findings

### 📌 1. Data Cleaning & Preprocessing
- Handled missing values across **8 key features** including reviews and host details
- Removed outliers using **IQR filtering** for numerical features like `log_price` and `review_scores_rating`

### 🛠️ 2. Feature Engineering
- **Amenity Count**: Calculated total number of amenities per listing
- **Host Days Active**: Derived from `host_since` date
- **Neighborhood Popularity**: Based on number of listings per neighborhood

### 📊 3. Model Training & Tuning
- **Model Used:** `RandomForestRegressor`
- **Hyperparameter Tuning:** Performed with `GridSearchCV` using 5-fold CV
- **Best Model Performance:**
  - ✅ RMSE: **0.3929**
  - ✅ MAE: **0.2978**
  - ✅ R²: **0.496**

### 📈 4. Feature Importance
Top predictors of price:
1. **Neighborhood Popularity**
2. **Number of Reviews**
3. **Amenities Count**
4. **Room Type**
5. **City**

### 📉 5. Visualization
- Predicted vs Actual prices plotted with a regression line
- Heatmap of correlations between key variables
- Feature importance displayed using a horizontal bar chart

---

## 🧠 Conclusions

- The model explained nearly **50% of the variance** in Airbnb prices using engineered and cleaned data.
- Features such as **amenities, reviews, and location popularity** are strong indicators of listing price.
- The project provides a blueprint for pricing optimization for hosts and Airbnb’s recommendation system.

---
