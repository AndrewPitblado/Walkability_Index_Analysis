"""Random Forest Analysis with Optuna Optimization - Top 20 Features
Uses top 20 features from previous analysis for faster hyperparameter tuning
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
import optuna
from optuna.visualization import plot_optimization_history, plot_param_importances

# ============================================================================
# LOAD DATA AND TOP 20 FEATURES
# ============================================================================

print("Loading dataset...")
data = pd.read_csv('EPA_SmartLocationDatabase_V3_CLEANED_NORMALIZED.csv')
print("Dataset loaded successfully.")

# Load your previously saved feature importances to get top 20
print("\nLoading top 20 features from previous analysis...")
feature_importance = pd.read_csv('feature_importance_walkability.csv')
top_20_features = feature_importance.head(20)['Feature'].tolist()

print(f"Using top 20 features:")
for i, feat in enumerate(top_20_features, 1):
    print(f"  {i}. {feat}")

# ============================================================================
# PREPARE DATA
# ============================================================================

target_col = 'NatWalkInd'

# Remove rows where target is missing
df_model = data[data[target_col].notna()].copy()
print(f"\nRemoved {len(data) - len(df_model):,} rows with missing target variable.")

# Create feature matrix with ONLY top 20 features
X = df_model[top_20_features].copy()
y = df_model[target_col]

# Handle any missing values
if X.isnull().sum().sum() > 0:
    print(f"Filling {X.isnull().sum().sum()} missing values with median...")
    X = X.fillna(X.median())

print(f"\nFeature matrix shape: {X.shape}")
print(f"Target variable shape: {y.shape}")

# ============================================================================
# TRAIN/TEST SPLIT
# ============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set: {X_train.shape[0]:,} samples")
print(f"Test set: {X_test.shape[0]:,} samples")

# ============================================================================
# OPTUNA HYPERPARAMETER OPTIMIZATION
# ============================================================================

print("\n" + "="*80)
print("OPTUNA HYPERPARAMETER OPTIMIZATION")
print("="*80)

def objective(trial):
    """
    Objective function for Optuna to optimize Random Forest hyperparameters
    """
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500, step=50),
        'max_depth': trial.suggest_int('max_depth', 10, 50, step=5),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
        'max_samples': trial.suggest_float('max_samples', 0.5, 1.0),
        'random_state': 42,
        'n_jobs': -1
    }
    
    # Create model
    rf = RandomForestRegressor(**params)
    
    # Use 3-fold CV for speed (you can increase to 5 if you want)
    cv_scores = cross_val_score(rf, X_train, y_train, cv=3, scoring='r2', n_jobs=-1)
    
    return cv_scores.mean()

# Create Optuna study
print("\nStarting hyperparameter optimization...")
print("Using top 20 features for faster optimization...")
print(f"Running {20} trials (adjust n_trials if needed)...\n")

study = optuna.create_study(
    direction='maximize',
    study_name='rf_walkability_top20_optimization',
    sampler=optuna.samplers.TPESampler(seed=42)
)

# Run optimization
study.optimize(objective, n_trials=20, show_progress_bar=True)

# ============================================================================
# OPTIMIZATION RESULTS
# ============================================================================

print("\n" + "="*80)
print("OPTIMIZATION RESULTS")
print("="*80)

print(f"\nBest trial: #{study.best_trial.number}")
print(f"Best cross-validation R²: {study.best_trial.value:.4f}")

print("\nBest hyperparameters:")
for key, value in study.best_params.items():
    print(f"  {key}: {value}")

# Save optimization results
optimization_results = pd.DataFrame({
    'Trial': [trial.number for trial in study.trials],
    'R2_Score': [trial.value for trial in study.trials],
    **{f'param_{key}': [trial.params.get(key) for trial in study.trials] 
       for key in study.best_params.keys()}
})
optimization_results.to_csv('optuna_optimization_results_top20.csv', index=False)
print("\n✓ Saved: optuna_optimization_results_top20.csv")

# Visualize optimization (requires plotly and kaleido)
try:
    fig1 = plot_optimization_history(study)
    fig1.write_image('optuna_optimization_history_top20.png', width=1000, height=600)
    print("✓ Saved: optuna_optimization_history_top20.png")
except Exception as e:
    print(f"Note: Could not save optimization history plot: {e}")
    print("  Install with: pip install plotly kaleido")

try:
    fig2 = plot_param_importances(study)
    fig2.write_image('optuna_param_importances_top20.png', width=1000, height=600)
    print("✓ Saved: optuna_param_importances_top20.png")
except Exception as e:
    print(f"Note: Could not save param importance plot: {e}")

# ============================================================================
# TRAIN OPTIMIZED MODEL
# ============================================================================

print("\n" + "="*80)
print("TRAINING OPTIMIZED MODEL")
print("="*80)

print("Training Random Forest with optimized hyperparameters...")
rf_optimized = RandomForestRegressor(**study.best_params, random_state=42, n_jobs=-1, verbose=1)
rf_optimized.fit(X_train, y_train)
print("Training complete.")

# ============================================================================
# EVALUATE OPTIMIZED MODEL
# ============================================================================

print("\nEvaluating optimized model...")

# Predictions
y_train_pred = rf_optimized.predict(X_train)
y_test_pred = rf_optimized.predict(X_test)

# Metrics
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_mae = mean_absolute_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)

test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_mae = mean_absolute_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)

print(f"\nOptimized Model - Training Set:")
print(f"  RMSE: {train_rmse:.4f}")
print(f"  MAE: {train_mae:.4f}")
print(f"  R²: {train_r2:.4f}")

print(f"\nOptimized Model - Test Set:")
print(f"  RMSE: {test_rmse:.4f}")
print(f"  MAE: {test_mae:.4f}")
print(f"  R²: {test_r2:.4f}")

# Cross-validation
print("\nPerforming 5-fold cross-validation...")
cv_scores = cross_val_score(rf_optimized, X_train, y_train, cv=5, scoring='r2', n_jobs=-1)
print(f"CV R² scores: {cv_scores}")
print(f"Mean CV R²: {np.mean(cv_scores):.4f} ± {np.std(cv_scores) * 2:.4f}")



# ============================================================================
# FEATURE IMPORTANCE (from optimized model)
# ============================================================================

print("\n" + "="*80)
print("FEATURE IMPORTANCE (Optimized Top 20 Model)")
print("="*80)

feature_importance_opt = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_optimized.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nFeature importances (ranked):")
print(feature_importance_opt.to_string(index=False))

feature_importance_opt.to_csv('feature_importance_optimized_top20.csv', index=False)
print("\n✓ Saved: feature_importance_optimized_top20.csv")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

print("\nGenerating visualizations...")

# 1. Feature Importance
plt.figure(figsize=(10, 6))
sns.barplot(data=feature_importance_opt, x='Importance', y='Feature', palette='viridis')
plt.title('Feature Importances - Optimized Top 20 Model')
plt.tight_layout()
plt.savefig('feature_importance_optimized_top20.png', dpi=300, bbox_inches='tight')
print("✓ Saved: feature_importance_optimized_top20.png")

# 2. Actual vs Predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_test_pred, alpha=0.3, s=1)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
         'r--', lw=2, label='Perfect Prediction')
plt.xlabel('Actual Walkability Index')
plt.ylabel('Predicted Walkability Index')
plt.title(f'Actual vs Predicted - Optimized Model (Top 20 Features)\nR² = {test_r2:.4f}')
plt.legend()
plt.tight_layout()
plt.savefig('actual_vs_predicted_optimized_top20.png', dpi=300, bbox_inches='tight')
print("✓ Saved: actual_vs_predicted_optimized_top20.png")

# 3. Residuals
plt.figure(figsize=(10, 6))
residuals = y_test - y_test_pred
plt.scatter(y_test_pred, residuals, alpha=0.3, s=1)
plt.axhline(y=0, color='r', linestyle='--', lw=2)
plt.xlabel('Predicted Walkability Index')
plt.ylabel('Residuals')
plt.title('Residual Plot - Optimized Model (Top 20 Features)')
plt.tight_layout()
plt.savefig('residuals_optimized_top20.png', dpi=300, bbox_inches='tight')
print("✓ Saved: residuals_optimized_top20.png")

# 4. Optimization trials plot
plt.figure(figsize=(12, 6))
plt.plot(optimization_results['Trial'], optimization_results['R2_Score'], 'o-', alpha=0.6)
plt.axhline(y=study.best_trial.value, color='r', linestyle='--', 
            label=f'Best R² = {study.best_trial.value:.4f}')
plt.xlabel('Trial Number')
plt.ylabel('Cross-Validation R² Score')
plt.title('Optuna Optimization Progress')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('optimization_progress.png', dpi=300, bbox_inches='tight')
print("✓ Saved: optimization_progress.png")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)

print(f"\nOptimized Model Summary:")
print(f"  Features: 20 (top features from previous analysis)")
print(f"  Optimization trials: {len(study.trials)}")
print(f"  Best CV R²: {study.best_trial.value:.4f}")
print(f"  Test R²: {test_r2:.4f}")
print(f"  Test RMSE: {test_rmse:.4f}")
print(f"  Test MAE: {test_mae:.4f}")

print(f"\nBest hyperparameters:")
for key, value in study.best_params.items():
    print(f"  {key}: {value}")

print(f"\nFiles created:")
print(f"  1. optuna_optimization_results_top20.csv")
print(f"  2. feature_importance_optimized_top20.csv")
print(f"  3. feature_importance_optimized_top20.png")
print(f"  4. actual_vs_predicted_optimized_top20.png")
print(f"  5. residuals_optimized_top20.png")
print(f"  6. optimization_progress.png")

plt.close('all')

print("\n" + "="*80)
print("Next Steps:")
print("  1. Compare test R² with your previous full model")
print("  2. If performance is similar, the top 20 features are sufficient")
print("  3. If you want even faster training, try reducing n_estimators")
print("  4. Consider testing without D5 metrics if you suspect leakage")
print("="*80)