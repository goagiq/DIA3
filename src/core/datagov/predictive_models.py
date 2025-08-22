"""
Predictive Models for Data.gov Integration - Phase 3
Implements machine learning models for trade forecasting, economic trends, and policy impact assessment.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.feature_selection import SelectKBest, f_regression
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class PredictiveModelingEngine:
    """Advanced predictive modeling engine for Data.gov data analysis."""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_selectors = {}
        self.model_metrics = {}
        self.model_path = "models/datagov/"
        os.makedirs(self.model_path, exist_ok=True)
        
        # Initialize model types
        self.model_types = {
            'trade_forecast': {
                'model': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'scaler': StandardScaler(),
                'features': 20
            },
            'economic_trends': {
                'model': RandomForestRegressor(n_estimators=200, random_state=42),
                'scaler': StandardScaler(),
                'features': 15
            },
            'policy_impact': {
                'model': Ridge(alpha=1.0),
                'scaler': MinMaxScaler(),
                'features': 10
            },
            'gdp_forecast': {
                'model': GradientBoostingRegressor(n_estimators=150, random_state=42),
                'scaler': StandardScaler(),
                'features': 12
            },
            'trade_balance': {
                'model': RandomForestRegressor(n_estimators=100, random_state=42),
                'scaler': StandardScaler(),
                'features': 18
            }
        }
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all predictive models."""
        for model_name, config in self.model_types.items():
            self.models[model_name] = config['model']
            self.scalers[model_name] = config['scaler']
            self.feature_selectors[model_name] = SelectKBest(score_func=f_regression, k=config['features'])
            self.model_metrics[model_name] = {}
    
    async def prepare_trade_data(self, historical_data: List[Dict[str, Any]]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare trade data for modeling."""
        try:
            df = pd.DataFrame(historical_data)
            
            # Feature engineering for trade data
            features = []
            for _, row in df.iterrows():
                feature_vector = [
                    row.get('import_value', 0),
                    row.get('export_value', 0),
                    row.get('trade_balance', 0),
                    row.get('month', 1),
                    row.get('year', 2020),
                    row.get('gdp_growth', 0),
                    row.get('inflation_rate', 0),
                    row.get('exchange_rate', 1),
                    row.get('political_stability', 0),
                    row.get('trade_policy_score', 0),
                    # Add lagged features
                    row.get('import_value_lag1', 0),
                    row.get('export_value_lag1', 0),
                    row.get('trade_balance_lag1', 0),
                    # Add seasonal features
                    np.sin(2 * np.pi * row.get('month', 1) / 12),
                    np.cos(2 * np.pi * row.get('month', 1) / 12),
                    # Add interaction features
                    row.get('import_value', 0) * row.get('gdp_growth', 0),
                    row.get('export_value', 0) * row.get('exchange_rate', 1),
                    row.get('trade_balance', 0) * row.get('political_stability', 0),
                    # Add trend features
                    row.get('year', 2020) - 2010,  # Years since 2010
                    row.get('quarter', 1)
                ]
                features.append(feature_vector)
            
            X = np.array(features)
            y = np.array([row.get('next_month_trade_balance', 0) for _, row in df.iterrows()])
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error preparing trade data: {e}")
            return np.array([]), np.array([])
    
    async def prepare_economic_data(self, historical_data: List[Dict[str, Any]]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare economic data for modeling."""
        try:
            df = pd.DataFrame(historical_data)
            
            # Feature engineering for economic data
            features = []
            for _, row in df.iterrows():
                feature_vector = [
                    row.get('gdp', 0),
                    row.get('gdp_growth', 0),
                    row.get('inflation_rate', 0),
                    row.get('unemployment_rate', 0),
                    row.get('interest_rate', 0),
                    row.get('exchange_rate', 1),
                    row.get('population', 0),
                    row.get('consumer_confidence', 0),
                    row.get('business_confidence', 0),
                    row.get('fiscal_balance', 0),
                    row.get('current_account_balance', 0),
                    row.get('foreign_direct_investment', 0),
                    # Add lagged features
                    row.get('gdp_lag1', 0),
                    row.get('inflation_lag1', 0),
                    row.get('unemployment_lag1', 0),
                    # Add trend features
                    row.get('year', 2020) - 2010,
                    row.get('quarter', 1)
                ]
                features.append(feature_vector)
            
            X = np.array(features)
            y = np.array([row.get('next_quarter_gdp_growth', 0) for _, row in df.iterrows()])
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error preparing economic data: {e}")
            return np.array([]), np.array([])
    
    async def prepare_policy_data(self, historical_data: List[Dict[str, Any]]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare policy impact data for modeling."""
        try:
            df = pd.DataFrame(historical_data)
            
            # Feature engineering for policy impact data
            features = []
            for _, row in df.iterrows():
                feature_vector = [
                    row.get('policy_change_score', 0),
                    row.get('trade_policy_score', 0),
                    row.get('fiscal_policy_score', 0),
                    row.get('monetary_policy_score', 0),
                    row.get('regulatory_score', 0),
                    row.get('political_stability', 0),
                    row.get('economic_freedom', 0),
                    row.get('corruption_perception', 0),
                    row.get('rule_of_law', 0),
                    row.get('government_effectiveness', 0),
                    # Add interaction features
                    row.get('policy_change_score', 0) * row.get('political_stability', 0),
                    row.get('trade_policy_score', 0) * row.get('economic_freedom', 0)
                ]
                features.append(feature_vector)
            
            X = np.array(features)
            y = np.array([row.get('economic_impact_score', 0) for _, row in df.iterrows()])
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error preparing policy data: {e}")
            return np.array([]), np.array([])
    
    async def train_trade_forecast_model(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train trade forecasting model."""
        try:
            logger.info("Training trade forecast model...")
            
            X, y = await self.prepare_trade_data(historical_data)
            
            if len(X) == 0 or len(y) == 0:
                return {"status": "error", "message": "Insufficient data for training"}
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Feature selection
            X_train_selected = self.feature_selectors['trade_forecast'].fit_transform(X_train, y_train)
            X_test_selected = self.feature_selectors['trade_forecast'].transform(X_test)
            
            # Scale features
            X_train_scaled = self.scalers['trade_forecast'].fit_transform(X_train_selected)
            X_test_scaled = self.scalers['trade_forecast'].transform(X_test_selected)
            
            # Train model
            self.models['trade_forecast'].fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = self.models['trade_forecast'].predict(X_test_scaled)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(self.models['trade_forecast'], X_train_scaled, y_train, cv=5)
            
            # Store metrics
            self.model_metrics['trade_forecast'] = {
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            # Save model
            await self._save_model('trade_forecast')
            
            logger.info(f"Trade forecast model trained successfully. R²: {r2:.4f}")
            
            return {
                "status": "success",
                "model": "trade_forecast",
                "metrics": self.model_metrics['trade_forecast'],
                "message": "Trade forecast model trained successfully"
            }
            
        except Exception as e:
            logger.error(f"Error training trade forecast model: {e}")
            return {"status": "error", "message": str(e)}
    
    async def train_economic_trends_model(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train economic trends prediction model."""
        try:
            logger.info("Training economic trends model...")
            
            X, y = await self.prepare_economic_data(historical_data)
            
            if len(X) == 0 or len(y) == 0:
                return {"status": "error", "message": "Insufficient data for training"}
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Feature selection
            X_train_selected = self.feature_selectors['economic_trends'].fit_transform(X_train, y_train)
            X_test_selected = self.feature_selectors['economic_trends'].transform(X_test)
            
            # Scale features
            X_train_scaled = self.scalers['economic_trends'].fit_transform(X_train_selected)
            X_test_scaled = self.scalers['economic_trends'].transform(X_test_selected)
            
            # Train model
            self.models['economic_trends'].fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = self.models['economic_trends'].predict(X_test_scaled)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(self.models['economic_trends'], X_train_scaled, y_train, cv=5)
            
            # Store metrics
            self.model_metrics['economic_trends'] = {
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            # Save model
            await self._save_model('economic_trends')
            
            logger.info(f"Economic trends model trained successfully. R²: {r2:.4f}")
            
            return {
                "status": "success",
                "model": "economic_trends",
                "metrics": self.model_metrics['economic_trends'],
                "message": "Economic trends model trained successfully"
            }
            
        except Exception as e:
            logger.error(f"Error training economic trends model: {e}")
            return {"status": "error", "message": str(e)}
    
    async def train_policy_impact_model(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train policy impact assessment model."""
        try:
            logger.info("Training policy impact model...")
            
            X, y = await self.prepare_policy_data(historical_data)
            
            if len(X) == 0 or len(y) == 0:
                return {"status": "error", "message": "Insufficient data for training"}
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Feature selection
            X_train_selected = self.feature_selectors['policy_impact'].fit_transform(X_train, y_train)
            X_test_selected = self.feature_selectors['policy_impact'].transform(X_test)
            
            # Scale features
            X_train_scaled = self.scalers['policy_impact'].fit_transform(X_train_selected)
            X_test_scaled = self.scalers['policy_impact'].transform(X_test_selected)
            
            # Train model
            self.models['policy_impact'].fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = self.models['policy_impact'].predict(X_test_scaled)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(self.models['policy_impact'], X_train_scaled, y_train, cv=5)
            
            # Store metrics
            self.model_metrics['policy_impact'] = {
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            # Save model
            await self._save_model('policy_impact')
            
            logger.info(f"Policy impact model trained successfully. R²: {r2:.4f}")
            
            return {
                "status": "success",
                "model": "policy_impact",
                "metrics": self.model_metrics['policy_impact'],
                "message": "Policy impact model trained successfully"
            }
            
        except Exception as e:
            logger.error(f"Error training policy impact model: {e}")
            return {"status": "error", "message": str(e)}
    
    async def forecast_trade_flows(self, input_data: Dict[str, Any], forecast_periods: int = 12) -> Dict[str, Any]:
        """Forecast trade flows using trained model."""
        try:
            if 'trade_forecast' not in self.models:
                return {"status": "error", "message": "Trade forecast model not trained"}
            
            # Prepare input features
            features = self._prepare_forecast_features(input_data, 'trade_forecast')
            
            if len(features) == 0:
                return {"status": "error", "message": "Invalid input data"}
            
            # Feature selection and scaling
            features_selected = self.feature_selectors['trade_forecast'].transform(features)
            features_scaled = self.scalers['trade_forecast'].transform(features_selected)
            
            # Make prediction
            prediction = self.models['trade_forecast'].predict(features_scaled)[0]
            
            # Generate confidence interval (simplified)
            confidence_interval = prediction * 0.1  # 10% margin
            
            return {
                "status": "success",
                "prediction": float(prediction),
                "confidence_interval": {
                    "lower": float(prediction - confidence_interval),
                    "upper": float(prediction + confidence_interval)
                },
                "forecast_periods": forecast_periods,
                "model_metrics": self.model_metrics.get('trade_forecast', {}),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error forecasting trade flows: {e}")
            return {"status": "error", "message": str(e)}
    
    async def predict_economic_indicators(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict economic indicators using trained model."""
        try:
            if 'economic_trends' not in self.models:
                return {"status": "error", "message": "Economic trends model not trained"}
            
            # Prepare input features
            features = self._prepare_forecast_features(input_data, 'economic_trends')
            
            if len(features) == 0:
                return {"status": "error", "message": "Invalid input data"}
            
            # Feature selection and scaling
            features_selected = self.feature_selectors['economic_trends'].transform(features)
            features_scaled = self.scalers['economic_trends'].transform(features_selected)
            
            # Make prediction
            prediction = self.models['economic_trends'].predict(features_scaled)[0]
            
            # Generate confidence interval
            confidence_interval = prediction * 0.15  # 15% margin
            
            return {
                "status": "success",
                "prediction": float(prediction),
                "confidence_interval": {
                    "lower": float(prediction - confidence_interval),
                    "upper": float(prediction + confidence_interval)
                },
                "model_metrics": self.model_metrics.get('economic_trends', {}),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error predicting economic indicators: {e}")
            return {"status": "error", "message": str(e)}
    
    async def assess_policy_impact(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess policy impact using trained model."""
        try:
            if 'policy_impact' not in self.models:
                return {"status": "error", "message": "Policy impact model not trained"}
            
            # Prepare input features
            features = self._prepare_forecast_features(policy_data, 'policy_impact')
            
            if len(features) == 0:
                return {"status": "error", "message": "Invalid input data"}
            
            # Feature selection and scaling
            features_selected = self.feature_selectors['policy_impact'].transform(features)
            features_scaled = self.scalers['policy_impact'].transform(features_selected)
            
            # Make prediction
            prediction = self.models['policy_impact'].predict(features_scaled)[0]
            
            # Generate confidence interval
            confidence_interval = prediction * 0.2  # 20% margin
            
            # Interpret impact
            impact_level = self._interpret_policy_impact(prediction)
            
            return {
                "status": "success",
                "prediction": float(prediction),
                "impact_level": impact_level,
                "confidence_interval": {
                    "lower": float(prediction - confidence_interval),
                    "upper": float(prediction + confidence_interval)
                },
                "model_metrics": self.model_metrics.get('policy_impact', {}),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error assessing policy impact: {e}")
            return {"status": "error", "message": str(e)}
    
    def _prepare_forecast_features(self, input_data: Dict[str, Any], model_type: str) -> np.ndarray:
        """Prepare features for forecasting."""
        try:
            if model_type == 'trade_forecast':
                features = [
                    input_data.get('import_value', 0),
                    input_data.get('export_value', 0),
                    input_data.get('trade_balance', 0),
                    input_data.get('month', 1),
                    input_data.get('year', 2020),
                    input_data.get('gdp_growth', 0),
                    input_data.get('inflation_rate', 0),
                    input_data.get('exchange_rate', 1),
                    input_data.get('political_stability', 0),
                    input_data.get('trade_policy_score', 0),
                    input_data.get('import_value_lag1', 0),
                    input_data.get('export_value_lag1', 0),
                    input_data.get('trade_balance_lag1', 0),
                    np.sin(2 * np.pi * input_data.get('month', 1) / 12),
                    np.cos(2 * np.pi * input_data.get('month', 1) / 12),
                    input_data.get('import_value', 0) * input_data.get('gdp_growth', 0),
                    input_data.get('export_value', 0) * input_data.get('exchange_rate', 1),
                    input_data.get('trade_balance', 0) * input_data.get('political_stability', 0),
                    input_data.get('year', 2020) - 2010,
                    input_data.get('quarter', 1)
                ]
            elif model_type == 'economic_trends':
                features = [
                    input_data.get('gdp', 0),
                    input_data.get('gdp_growth', 0),
                    input_data.get('inflation_rate', 0),
                    input_data.get('unemployment_rate', 0),
                    input_data.get('interest_rate', 0),
                    input_data.get('exchange_rate', 1),
                    input_data.get('population', 0),
                    input_data.get('consumer_confidence', 0),
                    input_data.get('business_confidence', 0),
                    input_data.get('fiscal_balance', 0),
                    input_data.get('current_account_balance', 0),
                    input_data.get('foreign_direct_investment', 0),
                    input_data.get('gdp_lag1', 0),
                    input_data.get('inflation_lag1', 0),
                    input_data.get('unemployment_lag1', 0),
                    input_data.get('year', 2020) - 2010,
                    input_data.get('quarter', 1)
                ]
            elif model_type == 'policy_impact':
                features = [
                    input_data.get('policy_change_score', 0),
                    input_data.get('trade_policy_score', 0),
                    input_data.get('fiscal_policy_score', 0),
                    input_data.get('monetary_policy_score', 0),
                    input_data.get('regulatory_score', 0),
                    input_data.get('political_stability', 0),
                    input_data.get('economic_freedom', 0),
                    input_data.get('corruption_perception', 0),
                    input_data.get('rule_of_law', 0),
                    input_data.get('government_effectiveness', 0),
                    input_data.get('policy_change_score', 0) * input_data.get('political_stability', 0),
                    input_data.get('trade_policy_score', 0) * input_data.get('economic_freedom', 0)
                ]
            else:
                return np.array([])
            
            return np.array([features])
            
        except Exception as e:
            logger.error(f"Error preparing forecast features: {e}")
            return np.array([])
    
    def _interpret_policy_impact(self, prediction: float) -> str:
        """Interpret policy impact prediction."""
        if prediction > 0.7:
            return "Very Positive"
        elif prediction > 0.3:
            return "Positive"
        elif prediction > -0.3:
            return "Neutral"
        elif prediction > -0.7:
            return "Negative"
        else:
            return "Very Negative"
    
    async def _save_model(self, model_name: str):
        """Save trained model to disk."""
        try:
            model_file = os.path.join(self.model_path, f"{model_name}_model.pkl")
            scaler_file = os.path.join(self.model_path, f"{model_name}_scaler.pkl")
            selector_file = os.path.join(self.model_path, f"{model_name}_selector.pkl")
            metrics_file = os.path.join(self.model_path, f"{model_name}_metrics.json")
            
            # Save model components
            joblib.dump(self.models[model_name], model_file)
            joblib.dump(self.scalers[model_name], scaler_file)
            joblib.dump(self.feature_selectors[model_name], selector_file)
            
            # Save metrics
            import json
            with open(metrics_file, 'w') as f:
                json.dump(self.model_metrics[model_name], f)
            
            logger.info(f"Model {model_name} saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving model {model_name}: {e}")
    
    async def load_model(self, model_name: str) -> bool:
        """Load trained model from disk."""
        try:
            model_file = os.path.join(self.model_path, f"{model_name}_model.pkl")
            scaler_file = os.path.join(self.model_path, f"{model_name}_scaler.pkl")
            selector_file = os.path.join(self.model_path, f"{model_name}_selector.pkl")
            metrics_file = os.path.join(self.model_path, f"{model_name}_metrics.json")
            
            if not all(os.path.exists(f) for f in [model_file, scaler_file, selector_file, metrics_file]):
                return False
            
            # Load model components
            self.models[model_name] = joblib.load(model_file)
            self.scalers[model_name] = joblib.load(scaler_file)
            self.feature_selectors[model_name] = joblib.load(selector_file)
            
            # Load metrics
            import json
            with open(metrics_file, 'r') as f:
                self.model_metrics[model_name] = json.load(f)
            
            logger.info(f"Model {model_name} loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            return False
    
    async def get_model_metrics(self, model_name: str = None) -> Dict[str, Any]:
        """Get model performance metrics."""
        if model_name:
            return self.model_metrics.get(model_name, {})
        else:
            return self.model_metrics
    
    async def get_model_status(self) -> Dict[str, Any]:
        """Get status of all models."""
        status = {}
        for model_name in self.model_types.keys():
            status[model_name] = {
                "trained": model_name in self.models,
                "metrics": self.model_metrics.get(model_name, {}),
                "last_updated": datetime.now().isoformat()
            }
        return status
