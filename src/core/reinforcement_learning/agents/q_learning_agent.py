"""
Q-Learning Agent for Discrete Action Spaces
Implements Q-Learning algorithm for intelligence analysis applications
"""

import numpy as np
import logging
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class State:
    """State representation for RL environment"""
    features: np.ndarray
    metadata: Dict[str, Any]
    timestamp: float

@dataclass
class Action:
    """Action representation for RL environment"""
    action_id: str
    parameters: Dict[str, Any]
    confidence: float

@dataclass
class Reward:
    """Reward representation for RL environment"""
    value: float
    components: Dict[str, float]
    metadata: Dict[str, Any]

class QLearningAgent:
    """Q-Learning agent for discrete action spaces"""
    
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}
            
        self.name = "q_learning"
        self.q_table = {}
        self.learning_rate = config.get('learning_rate', 0.1)
        self.discount_factor = config.get('discount_factor', 0.95)
        self.epsilon = config.get('epsilon', 0.1)
        self.is_trained = False
        
        logger.info(f"Initialized Q-Learning agent with config: {config}")
        
    async def select_action(self, state: State) -> Action:
        """Select action using epsilon-greedy policy"""
        state_key = self._state_to_key(state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
            
        available_actions = list(self.q_table[state_key].keys())
        if not available_actions:
            available_actions = ["default_action"]
            
        if np.random.random() < self.epsilon:
            # Exploration: random action
            action_id = np.random.choice(available_actions)
            confidence = 0.5
        else:
            # Exploitation: best action
            if self.q_table[state_key]:
                action_id = max(self.q_table[state_key], key=self.q_table[state_key].get)
                confidence = 0.8
            else:
                action_id = "default_action"
                confidence = 0.3
                
        return Action(
            action_id=action_id,
            parameters={},
            confidence=confidence
        )
        
    async def update(self, state: State, action: Action, reward: Reward, next_state: State):
        """Update Q-values using Q-learning update rule"""
        state_key = self._state_to_key(state)
        next_state_key = self._state_to_key(next_state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {}
            
        current_q = self.q_table[state_key].get(action.action_id, 0.0)
        max_next_q = max(self.q_table[next_state_key].values()) if self.q_table[next_state_key] else 0.0
        
        new_q = current_q + self.learning_rate * (reward.value + self.discount_factor * max_next_q - current_q)
        self.q_table[state_key][action.action_id] = new_q
        
        logger.debug(f"Updated Q-value for state {state_key}, action {action.action_id}: {new_q}")
        
    async def train(self, training_data: List[Tuple[State, Action, Reward, State]]):
        """Train the agent on historical data"""
        logger.info(f"Training Q-Learning agent on {len(training_data)} samples")
        
        for state, action, reward, next_state in training_data:
            await self.update(state, action, reward, next_state)
            
        self.is_trained = True
        logger.info("Q-Learning agent training completed")
        
    def _state_to_key(self, state: State) -> str:
        """Convert state to hashable key"""
        return str(hash(tuple(state.features.flatten())))
        
    def get_q_table_size(self) -> int:
        """Get the size of the Q-table"""
        return len(self.q_table)
        
    def get_action_values(self, state: State) -> Dict[str, float]:
        """Get Q-values for all actions in a given state"""
        state_key = self._state_to_key(state)
        return self.q_table.get(state_key, {})
