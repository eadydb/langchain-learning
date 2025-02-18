"""Calculator service module."""
from typing import Dict, Any
from ..schemas.base import CalculationResponse

class CalculatorService:
    """Calculator service for basic arithmetic operations."""
    
    @staticmethod
    def calculate(operation: str, x: float, y: float) -> CalculationResponse:
        """
        Perform basic arithmetic calculation.
        
        Args:
            operation: Type of operation (+, -, *, /)
            x: First number
            y: Second number
            
        Returns:
            CalculationResponse: Result of calculation
            
        Raises:
            ValueError: If operation is not supported or division by zero
        """
        operations = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else float('inf')
        }
        
        if operation not in operations:
            raise ValueError(f"Unsupported operation: {operation}")
            
        result = operations[operation](x, y)
        return CalculationResponse(
            operation=operation,
            x=x,
            y=y,
            result=result
        )
