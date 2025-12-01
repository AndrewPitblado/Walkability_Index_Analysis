"""Random Forest Anaylsis for EPA Dataset.
Purpose: Predict National Walkability Index using Random Forest Regressor.

"""

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
print("Loading dataset...")
data = pd.read_csv('EPA_SmartLocationDatabase_V3_CLEANED_NORMALIZED.csv')
print("Dataset loaded successfully.")

# =============== Define Features to drop ===============

# Target variable
target_col = 'NatWalkInd'
# Columns to drop
cols_to_drop = [
    # Target variable
    target_col,
    # Identifiers
    'OBJECTID', 'GEOID', 'GEOID20', 'STATEFP', 'COUNTYFP',
    'TRACTCE', 'BLKGRPCE', 'CBSA', 'CBSA_Name', 'CSA', 'CSA_Name',

    # Spatial geometry
    'Shape_length', 'Shape_Area',

    # Ranked/percentile columns (Derived from original features)
    'D2A_Ranked', 'D2B_Ranked', 'D3B_Ranked', 'D4A_Ranked',

    #Regional aggregate data
    'CBSA_POP', 'CBSA_EMP', 'CBSA_WRK',

    # Categorical variables created from normalization
    'PopDensity_Category', 'EmpDensity_Category', 'Walkability_Category', 'Urban_Rural',

    # D5 accessibility metrics (optional - may test with/without)
    # Uncomment these if you want to exclude them:
    # 'D5AR', 'D5AE', 'D5BR', 'D5BE', 'D5CR', 'D5CRI', 
    # 'D5CE', 'D5CEI', 'D5DR', 'D5DRI', 'D5DE', 'D5DEI',
    # 'D5AR_normalized', 'D5AE_normalized',
]

# Remove columns that don't exist in the dataframe
cols_to_drop = [col for col in cols_to_drop if col in data.columns]
print(f"Dropping {len(cols_to_drop)} columns: {cols_to_drop}")


# =============== Prepare Data ===============
print("Preparing data...")

# Remove rows where target is missing

df_model = data[data[target_col].notna()].copy()
print (f"Removed {len(data) - len(df_model)} rows with missing target variable.")

# Create feature matrix X and target vector y 
X = df_model.drop(columns=cols_to_drop)
y = df_model[target_col]

# Handle any remaining missing values in features (if any)
print(f"\nFeature matrix shape: {X.shape}")
print(f"Feature columns with missing values:\n{X.isnull().sum().sum()}")

if X.isnull().sum().sum() > 0:
    X = X.fillna(X.median())
    print("Filled missing values in features with median.")

# Remove non-numeric columns if any 
numeric_cols = X.select_dtypes(include=[np.number]).columns
if len(numeric_cols) < len(X.columns):
    print(f"Removing non-numeric columns: {len(X.columns) - len(numeric_cols)}")
    X = X[numeric_cols]

print(f"Final feature matrix shape: {X.shape}")

# =============== Split Data ===============
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set size: {X_train.shape[0]} samples")
print(f"Testing set size: {X_test.shape[0]:,} samples")
# =============== Train Random Forest Regressor ===============
print("Training Random Forest Regressor...")
rf = RandomForestRegressor(n_estimators=100, 
                           random_state=42,
                           max_depth=20,
                           min_samples_split=10,
                            min_samples_leaf=5,
                            n_jobs=-1,
                            verbose=1,
                            max_features='sqrt'
                            )
rf.fit(X_train, y_train)

print("Model training complete.")

# =============== Evaluate Model ===============
print("Evaluating model...")

# Predictions
y_train_pred = rf.predict(X_train)
y_test_pred = rf.predict(X_test)

# Training metrics
train_mse = mean_squared_error(y_train, y_train_pred)
train_rmse = np.sqrt(train_mse)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)

# Testing metrics
test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)

print(f"\nTraining Set Metrics:")
print(f"RMSE: {train_rmse:.4f}")
print(f"MAE: {train_mae:.4f}")
print(f"R^2: {train_r2:.4f}")

print(f"\nTesting Set Metrics:")
print(f"RMSE: {test_rmse:.4f}")
print(f"MAE: {test_mae:.4f}")
print(f"R^2: {test_r2:.4f}")

# Cross-validation
print("\nPerforming cross-validation...")
cv_scores = cross_val_score(rf, X_train, y_train, cv=5, scoring='r2', n_jobs=-1)
print(f"Cross-validation R^2 scores: {cv_scores}")
print(f"Mean CV R^2: {np.mean(cv_scores):.4f} ± {np.std(cv_scores) * 2 :.4f}")


# =============== Feature Importance ===============
print("Calculating feature importances...")
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf.feature_importances_
}).sort_values(by='Importance', ascending=False)    
print("\nTop 20 Feature Importances:")
print(feature_importance.head(20).to_string(index=False))
# Save feature importances to CSV
feature_importance.to_csv('feature_importance_walkability.csv', index=False)
print("✓ Saved: feature_importance_walkability.csv")
# Plot feature importances
plt.figure(figsize=(10, 6))
sns.barplot(data=feature_importance.head(20), x='Importance', y='Feature', palette='viridis')
plt.title('Top 20 Feature Importances for Walkability Index Prediction')
plt.tight_layout()
plt.savefig('feature_importance_plot.png', dpi=300, bbox_inches='tight')
print("✓ Saved: feature_importance_plot.png")


# Visualizations 

print("Generating visualizations...")

# 1. Feature Importance Plot 
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_test_pred, alpha=0.3, s=1)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
         'r--', lw=2, label='Perfect Prediction')
plt.xlabel('Actual Walkability Index')
plt.ylabel('Predicted Walkability Index')
plt.title(f'Actual vs Predicted Walkability (Test Set)\nR² = {test_r2:.4f}')
plt.legend()
plt.tight_layout()
plt.savefig('actual_vs_predicted.png', dpi=300, bbox_inches='tight')
print("✓ Saved: actual_vs_predicted.png")

# 3. Residuals Plot
plt.figure(figsize=(10, 6))
residuals = y_test - y_test_pred
plt.scatter(y_test_pred, residuals, alpha=0.3, s=1)
plt.axhline(y=0, color='r', linestyle='--', lw=2)
plt.xlabel('Predicted Walkability Index')
plt.ylabel('Residuals')
plt.title('Residual Plot - Test Set')
plt.tight_layout()
plt.savefig('residuals_plot.png', dpi=300, bbox_inches='tight')
print("✓ Saved: residuals_plot.png")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"\nModel: Random Forest Regressor")
print(f"Features used: {X.shape[1]}")
print(f"Training samples: {X_train.shape[0]:,}")
print(f"Test samples: {X_test.shape[0]:,}")
print(f"\nTest Set Performance:")
print(f"  R² Score: {test_r2:.4f}")
print(f"  RMSE: {test_rmse:.4f} (on 1-20 scale)")
print(f"  MAE: {test_mae:.4f} (on 1-20 scale)")
print(f"\nFiles created:")
print(f"  1. feature_importance_walkability.csv")
print(f"  2. feature_importance_plot.png")
print(f"  3. actual_vs_predicted.png")
print(f"  4. residuals_plot.png")

plt.close('all')
