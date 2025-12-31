import json
import os
from datetime import datetime

class History:
    def __init__(self, history_file=".shodansploit_history"):
        self.history_file = history_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create history file if it doesn't exist."""
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)

    def add_entry(self, query_type, query, result_count=None):
        """
        Add a new entry to the history.
        
        Args:
            query_type: Type of query (e.g., 'host_search', 'exploit_cve')
            query: The actual query or search term
            result_count: Optional count of results
        """
        try:
            history = self.load()
            
            entry = {
                "timestamp": datetime.now().isoformat(),
                "type": query_type,
                "query": query,
                "result_count": result_count
            }
            
            history.append(entry)
            
            # Keep only last 100 entries
            if len(history) > 100:
                history = history[-100:]
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
        except Exception:
            return False

    def load(self):
        """Load history from file."""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def clear(self):
        """Clear all history."""
        with open(self.history_file, 'w') as f:
            json.dump([], f)

    def get_recent(self, count=10):
        """Get the most recent N entries."""
        history = self.load()
        return history[-count:]

    def search(self, keyword):
        """Search history for entries containing keyword."""
        history = self.load()
        keyword = keyword.lower()
        return [
            entry for entry in history
            if keyword in entry.get('query', '').lower() or keyword in entry.get('type', '').lower()
        ]
