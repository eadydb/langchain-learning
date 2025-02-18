"""Helper functions for the application."""
import json
import re
from typing import Dict, Any, Optional


def extract_json_from_response(response: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from a string response.
    
    Args:
        response: String containing JSON data.
        
    Returns:
        Extracted JSON data as a dictionary, or None if no valid JSON found.
    """
    # Try to find JSON in markdown code blocks
    json_match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON without markdown
    try:
        # Find the first occurrence of '{'
        start = response.find('{')
        if start != -1:
            # Find the last occurrence of '}'
            end = response.rfind('}')
            if end != -1:
                json_str = response[start:end + 1]
                return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    return None
