"""Base schemas for the application."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class WeatherResponse(BaseModel):
    """Weather response schema."""
    location: str
    temperature: str
    unit: str = Field(default="celsius")
    forecast: List[str]


class CalculationResponse(BaseModel):
    """Calculation response schema."""
    operation: str
    x: float
    y: float
    result: float


class OrderItem(BaseModel):
    """Order item schema."""
    order_id: str
    date: str
    product: str
    quantity: int
    price: float
    total: float
    status: str


class OrderResponse(BaseModel):
    """Order response schema."""
    user_id: str
    period: str
    total_orders: int
    orders: List[OrderItem]


class PackageFeature(BaseModel):
    """Package feature schema."""
    name: str
    description: Optional[str] = None


class Package(BaseModel):
    """Package schema."""
    id: str
    name: str
    price: float
    features: List[str]
    duration: str


class PackageResponse(BaseModel):
    """Package response schema."""
    package: Package
    qr_file: str
    payment_url: str


class QPSData(BaseModel):
    """QPS data point schema."""
    timestamp: datetime
    qps_value: float


class QPSResponse(BaseModel):
    """Response schema for QPS data."""
    status: str
    message: str
    data: List[QPSData]
