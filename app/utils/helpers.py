"""
AdGenius AI Backend - Helper Utilities
"""
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

def generate_id() -> str:
    """
    Generate a unique ID
    
    Returns:
        str: Unique ID
    """
    return str(uuid.uuid4())

def format_datetime(dt: datetime) -> str:
    """
    Format datetime to ISO 8601 string
    
    Args:
        dt (datetime): Datetime object
        
    Returns:
        str: Formatted datetime string
    """
    return dt.isoformat()

def parse_datetime(dt_str: str) -> datetime:
    """
    Parse ISO 8601 datetime string to datetime object
    
    Args:
        dt_str (str): Datetime string
        
    Returns:
        datetime: Datetime object
    """
    return datetime.fromisoformat(dt_str)

def to_json(obj: Any) -> str:
    """
    Convert object to JSON string
    
    Args:
        obj (Any): Object to convert
        
    Returns:
        str: JSON string
    """
    return json.dumps(obj, default=json_serializer)

def from_json(json_str: str) -> Any:
    """
    Convert JSON string to object
    
    Args:
        json_str (str): JSON string
        
    Returns:
        Any: Parsed object
    """
    return json.loads(json_str)

def json_serializer(obj: Any) -> Any:
    """
    JSON serializer for objects not serializable by default json code
    
    Args:
        obj (Any): Object to serialize
        
    Returns:
        Any: Serialized object
    """
    if isinstance(obj, datetime):
        return format_datetime(obj)
    
    raise TypeError(f"Type {type(obj)} not serializable")

def paginate(items: List[Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """
    Paginate a list of items
    
    Args:
        items (List[Any]): List of items to paginate
        page (int, optional): Page number. Defaults to 1.
        per_page (int, optional): Items per page. Defaults to 10.
        
    Returns:
        Dict[str, Any]: Pagination result
    """
    # Ensure page and per_page are valid
    page = max(1, page)
    per_page = max(1, min(100, per_page))
    
    # Calculate pagination
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total)
    
    # Get items for current page
    paginated_items = items[start_idx:end_idx]
    
    return {
        "items": paginated_items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "has_prev": page > 1,
            "has_next": page < total_pages
        }
    }

def filter_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
    """
    Filter dictionary to include only allowed keys
    
    Args:
        data (Dict[str, Any]): Dictionary to filter
        allowed_keys (List[str]): List of allowed keys
        
    Returns:
        Dict[str, Any]: Filtered dictionary
    """
    return {k: v for k, v in data.items() if k in allowed_keys}

def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries
    
    Args:
        dict1 (Dict[str, Any]): First dictionary
        dict2 (Dict[str, Any]): Second dictionary
        
    Returns:
        Dict[str, Any]: Merged dictionary
    """
    result = dict1.copy()
    result.update(dict2)
    return result
