"""
Phase 3: Advanced Ensemble Forecasting System
Advanced ensemble forecasting system for multi-model prediction.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
from loguru import logger

from .enhanced_time_series_models import TimeSeriesData, ForecastResult


@dataclass
class EnsembleForecastResult:
    """Result from ensemble forecasting."""
    predictions: np.ndarray
    confidence_intervals: Tuple[np.ndarray, np.ndarray]
    confidence_score: float
    model_weights: Dict[str, float]
    individual_predictions: Dict[str, np.ndarray]
    metadata: Dict[str, Any]
    timestamp: datetime


class MetaLearner:
    """Meta-learner for ensemble weight optimization."""
    
    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate
        self.weights = {}
        self.history = []
    
    async def optimize_weights(self, predictions: Dict[str, np.ndarray], 
                             actual_values: np.ndarray) -> Dict[str, float]:
        """Optimize ensemble weights using meta-learning."""
        try:
            # Initialize weights equally if not set
            if not self.weights:
                n_models = len(predictions)
                self.weights = {model: 1.0 / n_models for model in predictions.keys()}
            
            # Convert predictions to numpy arrays
            pred_arrays = {k: np.array(v) for k, v in predictions.items()}
            
            # Calculate weighted ensemble prediction
            ensemble_pred = np.zeros_like(actual_values)
            for model, pred in pred_arrays.items():
                ensemble_pred += self.weights[model] * pred
            
            # Calculate error
            error = np.mean((ensemble_pred - actual_values) ** 2)
            
            # Update weights using gradient descent
            for model, pred in pred_arrays.items():
                gradient = 2 * np.mean((ensemble_pred - actual_values) * pred)
                self.weights[model] -= self.learning_rate * gradient
            
            # Normalize weights to sum to 1
            total_weight = sum(self.weights.values())
            if total_weight > 0:
                self.weights = {k: v / total_weight for k, v in self.weights.items()}
            
            # Store history
            self.history.append({
                'weights': self.weights.copy(),
                'error': error,
                'timestamp': datetime.now()
            })
            
            logger.info(f"Meta-learner optimized weights: {self.weights}")
            return self.weights
            
        except Exception as e:
            logger.error(f"Error in meta-learner weight optimization: {e}")
            # Return equal weights as fallback
            n_models = len(predictions)
            return {model: 1.0 / n_models for model in predictions.keys()}


class EnsembleForecastingSystem:
    """Advanced ensemble forecasting system for Phase 3."""
    
    def __init__(self):
        self.base_models = {
            'lstm_advanced': 'LSTM Advanced',
            'transformer_forecast': 'Transformer Forecast',
            'temporal_fusion': 'Temporal Fusion Transformer',
            'informer': 'Informer Model',
            'autoformer': 'Autoformer Model'
        }
        self.meta_learner = MetaLearner()
        self.model_instances = {}
        self.ensemble_history = []
        
        logger.info("✅ Ensemble Forecasting System initialized")
    
    async def train_ensemble(self, training_data: TimeSeriesData) -> Dict[str, Any]:
        """Train ensemble of forecasting models."""
        try:
            logger.info("Training ensemble forecasting models...")
            
            # Import model components
            from .enhanced_time_series_models import EnhancedTimeSeriesModels
            
            # Initialize base models
            time_series_models = EnhancedTimeSeriesModels()
            
            # Train each base model
            training_results = {}
            for model_name in self.base_models.keys():
                try:
                    logger.info(f"Training model: {model_name}")
                    # Use the enhanced time series models for training
                    result = await time_series_models.train_model(
                        model_name=model_name,
                        data=training_data,
                        parameters={'ensemble_mode': True}
                    )
                    training_results[model_name] = result
                    logger.info(f"✅ Trained {model_name}: {result}")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to train {model_name}: {e}")
            
            # Store model instances
            self.model_instances = training_results
            
            # Initialize meta-learner with equal weights
            n_models = len(training_results)
            initial_weights = {model: 1.0 / n_models for model in training_results.keys()}
            self.meta_learner.weights = initial_weights
            
            logger.info(f"✅ Ensemble training completed with {len(training_results)} models")
            return {
                'success': True,
                'models_trained': len(training_results),
                'model_names': list(training_results.keys()),
                'initial_weights': initial_weights
            }
            
        except Exception as e:
            logger.error(f"Error in ensemble training: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def predict_ensemble(self, input_data: TimeSeriesData, 
                             horizon: int = 10) -> EnsembleForecastResult:
        """Generate ensemble predictions."""
        try:
            logger.info(f"Generating ensemble predictions with horizon {horizon}")
            
            # Import model components
            from .enhanced_time_series_models import EnhancedTimeSeriesModels
            
            # Initialize time series models
            time_series_models = EnhancedTimeSeriesModels()
            
            # Generate predictions from each model
            individual_predictions = {}
            for model_name in self.base_models.keys():
                try:
                    logger.info(f"Generating prediction for model: {model_name}")
                    # Use the enhanced time series models for prediction
                    forecast_result = await time_series_models.forecast_with_model(
                        model_name=model_name,
                        data=input_data,
                        horizon=horizon
                    )
                    individual_predictions[model_name] = forecast_result.predictions
                    logger.info(f"✅ Generated prediction for {model_name}: {len(forecast_result.predictions)} values")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to predict with {model_name}: {e}")
            
            logger.info(f"Generated predictions from {len(individual_predictions)} models")
            if not individual_predictions:
                raise ValueError("No models generated valid predictions")
            
            # Calculate ensemble prediction using current weights
            ensemble_pred = np.zeros(horizon)
            for model_name, prediction in individual_predictions.items():
                weight = self.meta_learner.weights.get(model_name, 1.0 / len(individual_predictions))
                ensemble_pred += weight * prediction
            
            # Calculate confidence intervals
            predictions_array = np.array(list(individual_predictions.values()))
            std_dev = np.std(predictions_array, axis=0)
            confidence_intervals = (
                ensemble_pred - 1.96 * std_dev,  # 95% confidence lower bound
                ensemble_pred + 1.96 * std_dev   # 95% confidence upper bound
            )
            
            # Calculate confidence score based on model agreement
            confidence_score = 1.0 - np.mean(std_dev) / np.mean(np.abs(ensemble_pred))
            confidence_score = max(0.0, min(1.0, confidence_score))
            
            # Create result
            result = EnsembleForecastResult(
                predictions=ensemble_pred,
                confidence_intervals=confidence_intervals,
                confidence_score=confidence_score,
                model_weights=self.meta_learner.weights.copy(),
                individual_predictions=individual_predictions,
                metadata={
                    'horizon': horizon,
                    'models_used': list(individual_predictions.keys()),
                    'ensemble_type': 'weighted_average'
                },
                timestamp=datetime.now()
            )
            
            # Store in history
            self.ensemble_history.append(result)
            
            logger.info(f"✅ Ensemble prediction completed with confidence score {confidence_score:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"Error in ensemble prediction: {e}")
            raise
    
    async def optimize_weights(self, validation_data: TimeSeriesData) -> Dict[str, float]:
        """Optimize ensemble weights using validation data."""
        try:
            logger.info("Optimizing ensemble weights...")
            
            # Generate predictions for validation data
            individual_predictions = {}
            for model_name in self.base_models.keys():
                try:
                    from .enhanced_time_series_models import EnhancedTimeSeriesModels
                    time_series_models = EnhancedTimeSeriesModels()
                    
                    forecast_result = await time_series_models.forecast_with_model(
                        model_name=model_name,
                        data=validation_data,
                        horizon=len(validation_data.values)
                    )
                    individual_predictions[model_name] = forecast_result.predictions
                except Exception as e:
                    logger.warning(f"⚠️ Failed to generate validation prediction for {model_name}: {e}")
            
            if not individual_predictions:
                raise ValueError("No models generated valid validation predictions")
            
            # Optimize weights using meta-learner
            actual_values = np.array(validation_data.values)
            optimized_weights = await self.meta_learner.optimize_weights(
                individual_predictions, actual_values
            )
            
            logger.info(f"✅ Ensemble weights optimized: {optimized_weights}")
            return optimized_weights
            
        except Exception as e:
            logger.error(f"Error in weight optimization: {e}")
            raise
    
    async def get_ensemble_status(self) -> Dict[str, Any]:
        """Get ensemble system status."""
        return {
            'status': 'operational',
            'base_models': self.base_models,
            'current_weights': self.meta_learner.weights,
            'history_length': len(self.ensemble_history),
            'meta_learner_history_length': len(self.meta_learner.history),
            'last_optimization': self.meta_learner.history[-1]['timestamp'] if self.meta_learner.history else None
        }
    
    async def reset_ensemble(self) -> Dict[str, Any]:
        """Reset ensemble to initial state."""
        try:
            # Reset meta-learner
            self.meta_learner.weights = {}
            self.meta_learner.history = []
            
            # Reset ensemble history
            self.ensemble_history = []
            
            # Reset model instances
            self.model_instances = {}
            
            logger.info("✅ Ensemble system reset to initial state")
            return {
                'success': True,
                'message': 'Ensemble system reset successfully'
            }
            
        except Exception as e:
            logger.error(f"Error resetting ensemble: {e}")
            return {
                'success': False,
                'error': str(e)
            }
