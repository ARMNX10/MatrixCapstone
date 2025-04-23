
"""
Calculator tool for evaluating mathematical expressions.
"""

def calculate_expression(expr: str) -> str:
    """Safely evaluate a math expression and return the result as a string."""
    try:
        # Restrict builtins for safety
        result = eval(expr, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"[Calculator Error] {e}"
