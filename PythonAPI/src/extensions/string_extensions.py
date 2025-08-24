import json
from typing import Optional, Any

class JsonString(str):
    def to_object(self) -> Optional[Any]:
        if not self:
            return None
        try:
            return json.loads(self)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None
