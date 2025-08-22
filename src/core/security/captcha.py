"""
CAPTCHA Service for Enhanced Report System.

This module provides CAPTCHA functionality for securing report access and preventing automated attacks.
"""

import base64
import io
import json
import logging
import math
import random
import string
import time
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CaptchaChallenge:
    """CAPTCHA challenge data structure."""
    challenge_id: str
    question: str
    answer: str
    created_at: datetime
    expires_at: datetime
    attempts: int = 0
    max_attempts: int = 3
    is_solved: bool = False
    difficulty: str = "medium"
    challenge_type: str = "text"


class CaptchaService:
    """
    CAPTCHA service for securing report access.
    
    Features:
    - Multiple challenge types (text, math, image)
    - Configurable difficulty levels
    - Rate limiting and attempt tracking
    - Time-based expiration
    - Secure answer verification
    """
    
    def __init__(self, challenge_timeout: int = 300, max_attempts: int = 3):
        """
        Initialize the CAPTCHA service.
        
        Args:
            challenge_timeout: Timeout for challenges in seconds
            max_attempts: Maximum attempts per challenge
        """
        self.challenge_timeout = challenge_timeout
        self.max_attempts = max_attempts
        self.active_challenges: Dict[str, CaptchaChallenge] = {}
        self.challenge_history: List[CaptchaChallenge] = []
        
        # Challenge templates
        self.text_challenges = [
            "What is the capital of France?",
            "What color is the sky?",
            "How many days are in a week?",
            "What is 2 + 2?",
            "What is the opposite of hot?",
            "What animal says 'meow'?",
            "What is the largest planet in our solar system?",
            "What is the chemical symbol for gold?",
            "What is the main ingredient in bread?",
            "What is the speed of light in miles per second?"
        ]
        
        self.text_answers = [
            "paris", "blue", "7", "4", "cold", "cat", "jupiter", "au", "flour", "186000"
        ]
        
        self.math_challenges = [
            ("What is 15 + 27?", "42"),
            ("What is 8 × 6?", "48"),
            ("What is 100 ÷ 4?", "25"),
            ("What is 13 - 7?", "6"),
            ("What is 3² + 4?", "13"),
            ("What is 20% of 50?", "10"),
            ("What is the square root of 16?", "4"),
            ("What is 5! (factorial)?", "120"),
            ("What is 2³ × 3?", "24"),
            ("What is 50 + 25 - 10?", "65")
        ]
        
        # Clean up expired challenges periodically
        self._cleanup_expired_challenges()
    
    def generate_challenge(self, challenge_type: str = "auto", 
                          difficulty: str = "medium") -> Dict[str, Any]:
        """
        Generate a new CAPTCHA challenge.
        
        Args:
            challenge_type: Type of challenge ("text", "math", "image", "auto")
            difficulty: Difficulty level ("easy", "medium", "hard")
            
        Returns:
            Dictionary containing challenge information
        """
        challenge_id = self._generate_challenge_id()
        
        if challenge_type == "auto":
            challenge_type = random.choice(["text", "math"])
        
        if challenge_type == "text":
            question, answer = self._generate_text_challenge(difficulty)
        elif challenge_type == "math":
            question, answer = self._generate_math_challenge(difficulty)
        elif challenge_type == "image":
            question, answer = self._generate_image_challenge(difficulty)
        else:
            raise ValueError(f"Unsupported challenge type: {challenge_type}")
        
        # Create challenge
        challenge = CaptchaChallenge(
            challenge_id=challenge_id,
            question=question,
            answer=answer.lower().strip(),
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=self.challenge_timeout),
            max_attempts=self.max_attempts,
            difficulty=difficulty,
            challenge_type=challenge_type
        )
        
        # Store challenge
        self.active_challenges[challenge_id] = challenge
        
        logger.info(f"Generated CAPTCHA challenge: {challenge_id} ({challenge_type})")
        
        return {
            "challenge_id": challenge_id,
            "question": question,
            "challenge_type": challenge_type,
            "difficulty": difficulty,
            "expires_at": challenge.expires_at.isoformat(),
            "max_attempts": self.max_attempts
        }
    
    def _generate_challenge_id(self) -> str:
        """Generate a unique challenge ID."""
        timestamp = str(int(time.time()))
        random_part = secrets.token_hex(8)
        return f"captcha_{timestamp}_{random_part}"
    
    def _generate_text_challenge(self, difficulty: str) -> Tuple[str, str]:
        """Generate a text-based challenge."""
        if difficulty == "easy":
            # Simple questions
            index = random.randint(0, len(self.text_challenges) - 1)
            return self.text_challenges[index], self.text_answers[index]
        elif difficulty == "medium":
            # Add some variation
            index = random.randint(0, len(self.text_challenges) - 1)
            question = self.text_challenges[index]
            answer = self.text_answers[index]
            
            # Add some noise to the question
            variations = [
                f"Please answer: {question}",
                f"Question: {question}",
                f"Can you tell me: {question}",
                f"I need to know: {question}"
            ]
            return random.choice(variations), answer
        else:  # hard
            # More complex questions
            complex_questions = [
                ("What is the sum of the first 5 prime numbers?", "28"),
                ("What is the product of 3, 4, and 5?", "60"),
                ("What is the remainder when 17 is divided by 5?", "2"),
                ("What is the next number in the sequence: 2, 4, 8, 16?", "32"),
                ("What is the value of π rounded to 2 decimal places?", "3.14")
            ]
            return random.choice(complex_questions)
    
    def _generate_math_challenge(self, difficulty: str) -> Tuple[str, str]:
        """Generate a math-based challenge."""
        if difficulty == "easy":
            # Simple arithmetic
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            operation = random.choice(["+", "-", "*"])
            
            if operation == "+":
                question = f"What is {a} + {b}?"
                answer = str(a + b)
            elif operation == "-":
                question = f"What is {a} - {b}?"
                answer = str(a - b)
            else:  # multiplication
                question = f"What is {a} × {b}?"
                answer = str(a * b)
                
        elif difficulty == "medium":
            # More complex operations
            a = random.randint(10, 50)
            b = random.randint(2, 10)
            operation = random.choice(["+", "-", "*", "/"])
            
            if operation == "+":
                question = f"What is {a} + {b}?"
                answer = str(a + b)
            elif operation == "-":
                question = f"What is {a} - {b}?"
                answer = str(a - b)
            elif operation == "*":
                question = f"What is {a} × {b}?"
                answer = str(a * b)
            else:  # division
                question = f"What is {a} ÷ {b}?"
                answer = str(a // b)
                
        else:  # hard
            # Complex mathematical operations
            operations = [
                ("What is 15² - 7²?", "176"),
                ("What is the square root of 144?", "12"),
                ("What is 5! ÷ 3!", "20"),
                ("What is 2³ + 3²?", "17"),
                ("What is 25% of 80?", "20")
            ]
            return random.choice(operations)
        
        return question, answer
    
    def _generate_image_challenge(self, difficulty: str) -> Tuple[str, str]:
        """Generate an image-based challenge (placeholder)."""
        # For now, return a text-based challenge
        # In a real implementation, this would generate actual images
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        color = random.choice(colors)
        
        question = f"What color is the circle in the image? (Type: {color})"
        answer = color
        
        return question, answer
    
    def verify_answer(self, challenge_id: str, user_answer: str) -> Dict[str, Any]:
        """
        Verify a user's answer to a CAPTCHA challenge.
        
        Args:
            challenge_id: ID of the challenge
            user_answer: User's answer
            
        Returns:
            Dictionary containing verification result
        """
        # Check if challenge exists
        if challenge_id not in self.active_challenges:
            return {
                "success": False,
                "error": "Challenge not found or expired",
                "challenge_id": challenge_id
            }
        
        challenge = self.active_challenges[challenge_id]
        
        # Check if challenge is expired
        if datetime.now() > challenge.expires_at:
            self._remove_challenge(challenge_id)
            return {
                "success": False,
                "error": "Challenge expired",
                "challenge_id": challenge_id
            }
        
        # Check if max attempts exceeded
        if challenge.attempts >= challenge.max_attempts:
            self._remove_challenge(challenge_id)
            return {
                "success": False,
                "error": "Maximum attempts exceeded",
                "challenge_id": challenge_id
            }
        
        # Increment attempt counter
        challenge.attempts += 1
        
        # Normalize answers for comparison
        normalized_user_answer = user_answer.lower().strip()
        normalized_correct_answer = challenge.answer.lower().strip()
        
        # Check if answer is correct
        is_correct = normalized_user_answer == normalized_correct_answer
        
        if is_correct:
            challenge.is_solved = True
            self._remove_challenge(challenge_id)
            
            logger.info(f"CAPTCHA challenge {challenge_id} solved successfully")
            
            return {
                "success": True,
                "message": "Challenge solved successfully",
                "challenge_id": challenge_id,
                "attempts_used": challenge.attempts
            }
        else:
            # Check if max attempts reached
            if challenge.attempts >= challenge.max_attempts:
                self._remove_challenge(challenge_id)
                return {
                    "success": False,
                    "error": "Maximum attempts exceeded",
                    "challenge_id": challenge_id,
                    "attempts_used": challenge.attempts
                }
            else:
                return {
                    "success": False,
                    "error": "Incorrect answer",
                    "challenge_id": challenge_id,
                    "attempts_remaining": challenge.max_attempts - challenge.attempts,
                    "attempts_used": challenge.attempts
                }
    
    def _remove_challenge(self, challenge_id: str):
        """Remove a challenge from active challenges and add to history."""
        if challenge_id in self.active_challenges:
            challenge = self.active_challenges.pop(challenge_id)
            self.challenge_history.append(challenge)
            
            # Keep only last 1000 challenges in history
            if len(self.challenge_history) > 1000:
                self.challenge_history = self.challenge_history[-1000:]
    
    def _cleanup_expired_challenges(self):
        """Remove expired challenges."""
        current_time = datetime.now()
        expired_challenges = []
        
        for challenge_id, challenge in self.active_challenges.items():
            if current_time > challenge.expires_at:
                expired_challenges.append(challenge_id)
        
        for challenge_id in expired_challenges:
            self._remove_challenge(challenge_id)
        
        if expired_challenges:
            logger.info(f"Cleaned up {len(expired_challenges)} expired challenges")
    
    def get_challenge_status(self, challenge_id: str) -> Dict[str, Any]:
        """
        Get the status of a CAPTCHA challenge.
        
        Args:
            challenge_id: ID of the challenge
            
        Returns:
            Dictionary containing challenge status
        """
        if challenge_id not in self.active_challenges:
            return {
                "exists": False,
                "error": "Challenge not found"
            }
        
        challenge = self.active_challenges[challenge_id]
        current_time = datetime.now()
        
        return {
            "exists": True,
            "challenge_id": challenge_id,
            "question": challenge.question,
            "challenge_type": challenge.challenge_type,
            "difficulty": challenge.difficulty,
            "created_at": challenge.created_at.isoformat(),
            "expires_at": challenge.expires_at.isoformat(),
            "is_expired": current_time > challenge.expires_at,
            "attempts_used": challenge.attempts,
            "attempts_remaining": challenge.max_attempts - challenge.attempts,
            "is_solved": challenge.is_solved,
            "time_remaining": max(0, (challenge.expires_at - current_time).total_seconds())
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get CAPTCHA service statistics."""
        current_time = datetime.now()
        
        # Active challenges
        active_count = len(self.active_challenges)
        expired_count = sum(1 for c in self.active_challenges.values() 
                          if current_time > c.expires_at)
        
        # Historical statistics
        total_challenges = len(self.challenge_history)
        solved_challenges = sum(1 for c in self.challenge_history if c.is_solved)
        failed_challenges = total_challenges - solved_challenges
        
        # Success rate
        success_rate = (solved_challenges / total_challenges * 100) if total_challenges > 0 else 0
        
        # Average attempts
        total_attempts = sum(c.attempts for c in self.challenge_history)
        avg_attempts = total_attempts / total_challenges if total_challenges > 0 else 0
        
        # Challenge type distribution
        type_distribution = {}
        for challenge in self.challenge_history:
            challenge_type = challenge.challenge_type
            type_distribution[challenge_type] = type_distribution.get(challenge_type, 0) + 1
        
        return {
            "active_challenges": active_count,
            "expired_challenges": expired_count,
            "total_challenges": total_challenges,
            "solved_challenges": solved_challenges,
            "failed_challenges": failed_challenges,
            "success_rate": round(success_rate, 2),
            "average_attempts": round(avg_attempts, 2),
            "challenge_type_distribution": type_distribution,
            "last_cleanup": current_time.isoformat()
        }
    
    def generate_report_access_captcha(self, report_id: str, user_id: str) -> Dict[str, Any]:
        """
        Generate a CAPTCHA challenge for report access.
        
        Args:
            report_id: ID of the report being accessed
            user_id: ID of the user requesting access
            
        Returns:
            Dictionary containing CAPTCHA challenge
        """
        # Generate a challenge with medium difficulty
        challenge_data = self.generate_challenge(
            challenge_type="auto",
            difficulty="medium"
        )
        
        # Add report-specific metadata
        challenge_data.update({
            "report_id": report_id,
            "user_id": user_id,
            "purpose": "report_access",
            "generated_at": datetime.now().isoformat()
        })
        
        logger.info(f"Generated report access CAPTCHA for report {report_id}, user {user_id}")
        
        return challenge_data
    
    def verify_report_access(self, challenge_id: str, user_answer: str, 
                           report_id: str, user_id: str) -> Dict[str, Any]:
        """
        Verify CAPTCHA for report access.
        
        Args:
            challenge_id: ID of the CAPTCHA challenge
            user_answer: User's answer
            report_id: ID of the report being accessed
            user_id: ID of the user requesting access
            
        Returns:
            Dictionary containing verification result
        """
        verification_result = self.verify_answer(challenge_id, user_answer)
        
        if verification_result["success"]:
            # Add report access metadata
            verification_result.update({
                "report_id": report_id,
                "user_id": user_id,
                "access_granted": True,
                "access_timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"Report access granted for report {report_id}, user {user_id}")
        else:
            verification_result.update({
                "report_id": report_id,
                "user_id": user_id,
                "access_granted": False
            })
            
            logger.warning(f"Report access denied for report {report_id}, user {user_id}")
        
        return verification_result
    
    def cleanup_old_history(self, days_to_keep: int = 30):
        """Clean up old challenge history."""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        original_count = len(self.challenge_history)
        self.challenge_history = [
            challenge for challenge in self.challenge_history
            if challenge.created_at > cutoff_date
        ]
        
        removed_count = original_count - len(self.challenge_history)
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old challenge records")


# Global CAPTCHA service instance
captcha_service = CaptchaService()
