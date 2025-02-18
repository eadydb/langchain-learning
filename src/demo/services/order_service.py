"""Order service module."""
from typing import Dict, List, Optional
from datetime import datetime
from ..schemas.base import OrderResponse, OrderItem

class OrderService:
    """Service for handling order operations."""
    
    def __init__(self):
        """Initialize the order service."""
        self._orders: Dict[str, Dict] = {}
        
    def create_order(self, order_id: str, items: List[Dict], user_id: str) -> OrderResponse:
        """
        Create a new order.
        
        Args:
            order_id: Unique order identifier
            items: List of items in the order
            user_id: ID of the user placing the order
            
        Returns:
            OrderResponse: Created order details
        """
        order = {
            'order_id': order_id,
            'items': items,
            'user_id': user_id,
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        self._orders[order_id] = order
        return OrderResponse(
            user_id=user_id,
            period="",
            total_orders=1,
            orders=[
                OrderItem(
                    order_id=order_id,
                    date=datetime.now().isoformat(),
                    product="",
                    quantity=0,
                    price=0.0,
                    total=0.0,
                    status="created"
                )
            ]
        )
        
    def get_order(self, order_id: str) -> Optional[OrderResponse]:
        """
        Retrieve order details by ID.
        
        Args:
            order_id: Order identifier
            
        Returns:
            Optional[OrderResponse]: Order details if found, None otherwise
        """
        order = self._orders.get(order_id)
        if order:
            return OrderResponse(
                user_id=order['user_id'],
                period="",
                total_orders=1,
                orders=[
                    OrderItem(
                        order_id=order_id,
                        date=order['created_at'],
                        product="",
                        quantity=0,
                        price=0.0,
                        total=0.0,
                        status=order['status']
                    )
                ]
            )
        return None

    def get_recent_orders(self, user_id: str, months: int = 3) -> OrderResponse:
        """
        Get recent orders for a user.
        
        Args:
            user_id: User ID to get orders for
            months: Number of months to look back
            
        Returns:
            OrderResponse: Recent order data
        """
        # Mock order data
        orders = [
            OrderItem(
                order_id=f"ORD-{i}",
                date=datetime.now().isoformat(),
                product=f"Product {i}",
                quantity=i,
                price=10.0 * i,
                total=10.0 * i * i,
                status="completed"
            )
            for i in range(1, 4)
        ]
        
        return OrderResponse(
            user_id=user_id,
            period=f"Last {months} months",
            total_orders=len(orders),
            orders=orders
        )
