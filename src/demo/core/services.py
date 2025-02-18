"""Core services for the application."""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random
import uuid
import qrcode
import os
from urllib.parse import urlencode
import numpy as np

from ..schemas.base import (
    WeatherResponse,
    CalculationResponse,
    OrderResponse,
    PackageResponse,
    Package,
    QPSResponse,
    QPSData
)


class WeatherService:
    """Service for weather-related operations."""
    
    @staticmethod
    def get_current_weather(location: str, unit: str = "celsius") -> WeatherResponse:
        """
        Get the current weather for a location.
        
        Args:
            location: The location to get weather for.
            unit: Temperature unit (celsius/fahrenheit).
            
        Returns:
            WeatherResponse object containing weather data.
        """
        # Mock weather data
        weather_data = WeatherResponse(
            location=location,
            temperature="22",
            unit=unit,
            forecast=["sunny", "windy"]
        )
        return weather_data


class CalculatorService:
    """Service for calculation operations."""
    
    @staticmethod
    def calculate(operation: str, x: float, y: float) -> CalculationResponse:
        """
        Perform basic arithmetic operations.
        
        Args:
            operation: Type of operation (add/subtract/multiply/divide).
            x: First number.
            y: Second number.
            
        Returns:
            CalculationResponse object containing the result.
            
        Raises:
            ValueError: If operation is invalid or division by zero.
        """
        operations = {
            "add": lambda: x + y,
            "subtract": lambda: x - y,
            "multiply": lambda: x * y,
            "divide": lambda: x / y if y != 0 else None
        }
        
        if operation not in operations:
            raise ValueError(f"Unknown operation: {operation}")
        
        result = operations[operation]()
        if result is None:
            raise ValueError("Division by zero")
            
        return CalculationResponse(
            operation=operation,
            x=x,
            y=y,
            result=result
        )


class OrderService:
    """Service for order-related operations."""
    
    @staticmethod
    def get_recent_orders(user_id: str, months: int = 3) -> OrderResponse:
        """
        Get recent orders for a user.
        
        Args:
            user_id: User ID to get orders for.
            months: Number of months to look back.
            
        Returns:
            OrderResponse object containing order data.
        """
        current_date = datetime.now()
        orders = []
        
        # Mock product data
        products = [
            {"name": "iPhone 15", "price": 6999},
            {"name": "MacBook Pro", "price": 12999},
            {"name": "AirPods Pro", "price": 1999},
            {"name": "iPad Air", "price": 4999},
            {"name": "Apple Watch", "price": 3299}
        ]
        
        statuses = ["已完成", "已发货", "待发货", "已取消"]
        
        # Generate random orders
        for _ in range(random.randint(3, 8)):
            order_date = current_date - timedelta(
                days=random.randint(0, months * 30)
            )
            product = random.choice(products)
            quantity = random.randint(1, 3)
            
            order = {
                "order_id": f"ORD-{random.randint(10000, 99999)}",
                "date": order_date.strftime("%Y-%m-%d"),
                "product": product["name"],
                "quantity": quantity,
                "price": product["price"],
                "total": product["price"] * quantity,
                "status": random.choice(statuses)
            }
            orders.append(order)
        
        # Sort orders by date
        orders.sort(key=lambda x: x["date"], reverse=True)
        
        return OrderResponse(
            user_id=user_id,
            period=f"最近{months}个月",
            total_orders=len(orders),
            orders=orders
        )


class PackageService:
    """Service for package-related operations."""
    
    def __init__(self):
        """Initialize the package service."""
        self.base_features = [
            "基础功能访问",
            "在线文档",
            "社区支持",
            "API访问",
            "数据分析",
            "高级报表",
            "专属支持",
            "定制化服务",
            "优先响应",
            "专家咨询"
        ]
    
    def create_custom_package(
        self,
        name: str,
        duration: int = 1,
        features: Optional[List[str]] = None,
        price: Optional[float] = None
    ) -> PackageResponse:
        """
        Create a custom package.
        
        Args:
            name: Package name.
            duration: Duration in months.
            features: List of features.
            price: Package price.
            
        Returns:
            PackageResponse object containing package data.
        """
        # Generate unique package ID
        package_id = str(uuid.uuid4())[:8]
        
        # Generate features if not provided
        if features is None:
            if price is None:
                price = 99
            feature_count = min(len(self.base_features), max(3, int(price / 100)))
            features = self.base_features[:feature_count]
        
        # Calculate price if not provided
        if price is None:
            base_price = len(features) * 30
            price = base_price * duration
        
        # Create package
        package = Package(
            id=package_id,
            name=name,
            price=price,
            features=features,
            duration=f"{duration}个月"
        )
        
        # Generate payment data
        payment_data = {
            "package_id": package_id,
            "package_name": name,
            "price": price,
            "duration": duration,
            "timestamp": datetime.now().strftime("%Y%m%d%H%M%S")
        }
        
        payment_url = f"https://example.com/pay?{urlencode(payment_data)}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(payment_url)
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Ensure output directory exists
        output_dir = "qrcodes"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save QR code
        qr_file = f"{output_dir}/package_{package_id}_{payment_data['timestamp']}.png"
        qr_image.save(qr_file)
        
        return PackageResponse(
            package=package,
            qr_file=qr_file,
            payment_url=payment_url
        )


class QPSService:
    """处理QPS相关操作的服务类"""
    
    def __init__(self):
        """初始化QPS服务"""
        self.base_qps = random.uniform(10, 50)  # 基础QPS值
        self.last_update = datetime.now()
        self.current_qps = self.base_qps
        
    def _generate_realistic_qps(self, timestamp: datetime) -> float:
        """
        生成真实感的QPS数据，考虑以下因素：
        1. 时间周期性（每天的高峰和低谷）
        2. 随机波动
        3. 突发流量
        
        Args:
            timestamp: 需要生成QPS数据的时间点
            
        Returns:
            float: 生成的QPS值
        """
        hour = timestamp.hour
        
        # 时间周期性因子 (0.5 到 1.5)
        # 早上9点到晚上10点是高峰期
        if 9 <= hour <= 22:
            time_factor = 1.0 + 0.5 * np.sin(np.pi * (hour - 9) / 13)
        else:
            time_factor = 0.5
            
        # 随机波动 (±20%)
        noise = random.uniform(0.8, 1.2)
        
        # 突发流量 (5%概率出现突发，流量增加50%-150%)
        if random.random() < 0.05:
            burst = random.uniform(1.5, 2.5)
        else:
            burst = 1.0
            
        # 计算最终QPS
        qps = self.base_qps * time_factor * noise * burst
        
        # 更新当前QPS（平滑过渡）
        time_diff = (timestamp - self.last_update).total_seconds()
        if time_diff > 0:
            # 使用指数移动平均使变化更平滑
            alpha = min(1.0, time_diff / 60)  # 一分钟内完成过渡
            self.current_qps = (1 - alpha) * self.current_qps + alpha * qps
            self.last_update = timestamp
            
        return round(self.current_qps, 2)
        
    def calculate_qps(self, time_window_minutes: int = 5, data_points: int = 10) -> QPSResponse:
        """
        计算指定时间窗口内的QPS数据，固定返回10个数据点
        
        Args:
            time_window_minutes: 需要查看的时间窗口（分钟）
            data_points: 已废弃，固定返回10个数据点
            
        Returns:
            QPSResponse: 包含QPS数据的响应对象，固定10个数据点
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=time_window_minutes)
        
        # 固定10个数据点
        data_points = 10
        
        # 创建时间点
        timestamps = [
            start_time + timedelta(seconds=i * (time_window_minutes * 60 / data_points))
            for i in range(data_points)
        ]
        
        # 生成QPS数据
        qps_data = []
        for ts in timestamps:
            qps = self._generate_realistic_qps(ts)
            qps_data.append(QPSData(
                timestamp=ts,
                qps_value=qps
            ))
        
        return QPSResponse(
            status="success",
            message=f"QPS数据获取成功（{time_window_minutes}分钟内，{data_points}个数据点）",
            data=qps_data
        )
