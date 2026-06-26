# Airbnb Listing Price & Rating Prediction
### Languages & Core:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=Plotly&logoColor=white)

This repository contains an end-to-end data science pipeline focused on data cleaning, exploratory analysis, and building predictive models to forecast both **listing prices** and **user ratings** across global markets.

## Project Scope
The analytical pipeline is split into two distinct execution environments to handle regional data variations:
* **Rio de Janeiro:** A localized study analyzing 40,769 entries. This pipeline includes robust data cleaning, outlier removal, and localized risk-assessment features (such as neighborhood safety metrics).
* **Global Cities:** A generalized pipeline built to scale across other cities worldwide. It maintains the core analytical structure but bypasses the specific Rio cleaning steps to respect unique global data distributions ($R^2$ performance ranges consistently from 0.40 to 0.60).

## Key Features
* **Data Cleaning & Preprocessing:** Handling missing values, targeted outlier filtering, and domain-specific feature engineering.
* **Exploratory Data Analysis (EDA):** Visualizations mapping out key market trends, geographical pricing concentrations, and feature correlations.
* **Segmented Price Prediction:** Regression modeling built dynamically around property room types to capture varying market mechanics.
* **Rating Modeling (WIP):** Benchmarking framework comparing multiclass classification vs. regression architectures to predict user satisfaction.

## Model Performance (Rio de Janeiro)

To predict listing prices, models were trained on the cleaned data and benchmarked against a Dummy Regressor baseline ($R^2 \approx 0.00$). Advanced algorithms like **XGBoost** and **Decision Trees** significantly outperformed baseline and linear shrinkage methods (**Lasso**).

### Overall Performance (Cleaned Dataset)
* **XGBoost Regressor:** $R^2 = 0.5169$
* **Decision Tree Regressor:** $R^2 = 0.4255$

### Segmented Analysis by Room Type
Market dynamics shift heavily based on the type of accommodation. Segmenting the data revealed that entire properties are far more predictable than shared spaces:

| Room Type | Decision Tree ($R^2$) | XGBoost ($R^2$) |
| :--- | :---: | :---: |
| **Entire home/apt** | 0.4200 | **0.4884** |
| **Private room** | 0.1375 | **0.2198** |
| **Shared room** | 0.0394 | **0.3219** |

---

## Work in Progress: Rating Prediction
The pipeline is currently being expanded to tackle user rating forecasting. The next phase will benchmark the performance of:
1. **Regression Models** (predicting exact continuous rating scores).
2. **Multiclass Classification Models** (predicting rating brackets/tiers).