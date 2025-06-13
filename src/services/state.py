"""
State management for user interactions.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class UserState:
    """User state data structure."""
    language: Optional[str] = None
    last_activity: Optional[datetime] = None
    request_count: int = 0


class StateManager:
    """Manages user states and interactions."""
    
    def __init__(self):
        self._user_states: Dict[int, UserState] = {}
    
    def get_user_state(self, user_id: int) -> UserState:
        """Get user state, creating if it doesn't exist."""
        if user_id not in self._user_states:
            self._user_states[user_id] = UserState()
        
        return self._user_states[user_id]
    
    def set_user_language(self, user_id: int, language: str):
        """Set the selected language for a user."""
        user_state = self.get_user_state(user_id)
        user_state.language = language
        user_state.last_activity = datetime.now()
        
        logger.info(f"User {user_id} selected language: {language}")
    
    def clear_user_language(self, user_id: int):
        """Clear the selected language for a user."""
        if user_id in self._user_states:
            self._user_states[user_id].language = None
            self._user_states[user_id].last_activity = datetime.now()
            
            logger.info(f"Cleared language selection for user {user_id}")
    
    def get_user_language(self, user_id: int) -> Optional[str]:
        """Get the selected language for a user."""
        return self.get_user_state(user_id).language
    
    def update_user_activity(self, user_id: int):
        """Update user's last activity timestamp."""
        user_state = self.get_user_state(user_id)
        user_state.last_activity = datetime.now()
        user_state.request_count += 1
    
    def cleanup_inactive_users(self, max_age_hours: int = 24):
        """Remove inactive users from state."""
        current_time = datetime.now()
        inactive_users = []
        
        for user_id, state in self._user_states.items():
            if state.last_activity:
                age = current_time - state.last_activity
                if age.total_seconds() > max_age_hours * 3600:
                    inactive_users.append(user_id)
        
        for user_id in inactive_users:
            del self._user_states[user_id]
            logger.info(f"Removed inactive user {user_id} from state")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about user states."""
        return {
            "total_users": len(self._user_states),
            "users_with_language": sum(1 for state in self._user_states.values() if state.language),
            "total_requests": sum(state.request_count for state in self._user_states.values())
        }


# Global state manager instance
state_manager = StateManager()
