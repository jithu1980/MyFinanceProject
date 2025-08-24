import json
from typing import Any
from datetime import datetime, date
from enum import Enum

def to_json(self: object) -> str:
    """
    Extension method to convert any object to JSON string.
    Usage: my_object.to_json()
    """
    def json_serializer(obj: Any) -> Any:
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.value
        elif hasattr(obj, '__dict__'):
            # For custom objects with __dict__ (like SQLAlchemy models)
            return {key: value for key, value in obj.__dict__.items() 
                   if not key.startswith('_')}
        elif hasattr(obj, 'model_dump'):
            # For Pydantic models
            return obj.model_dump()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    try:
        return json.dumps(self, default=json_serializer, indent=2)
    except Exception as e:
        print(f"JSON serialization error: {e}")
        return "{}"

def to_json_compact(self: object) -> str:
    """
    Extension method to convert any object to compact JSON string (no indentation).
    Usage: my_object.to_json_compact()
    """
    def json_serializer(obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.value
        elif hasattr(obj, '__dict__'):
            return {key: value for key, value in obj.__dict__.items() 
                   if not key.startswith('_')}
        elif hasattr(obj, 'model_dump'):
            return obj.model_dump()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    try:
        return json.dumps(self, default=json_serializer, separators=(',', ':'))
    except Exception as e:
        print(f"JSON serialization error: {e}")
        return "{}"

# Instead of monkey-patching built-in object, use these as utility functions.
# Example usage: json_str = to_json(my_object)
#                compact_json_str = to_json_compact(my_object)
