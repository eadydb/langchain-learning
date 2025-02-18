"""Package service module."""
from typing import Dict, List, Optional
import uuid
import qrcode
import os
from urllib.parse import urlencode
from ..schemas.base import Package, PackageResponse

class PackageService:
    """Service for managing package operations."""
    
    def __init__(self):
        """Initialize the package service."""
        self._packages: Dict[str, Dict] = {}
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
            name: Package name
            duration: Duration in months
            features: List of features
            price: Package price
            
        Returns:
            PackageResponse: Created package details
        """
        if features is None:
            features = self.base_features[:3]  # Basic features
            
        if price is None:
            price = len(features) * 100.0 * duration  # Basic pricing
            
        package_id = str(uuid.uuid4())
        package = Package(
            id=package_id,
            name=name,
            price=price,
            duration=duration,
            features=features
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        payment_data = {
            'id': package_id,
            'amount': price,
            'description': f"{name} Package for {duration} months"
        }
        qr.add_data(urlencode(payment_data))
        qr.make(fit=True)
        
        qr_file = f"qrcodes/package_{package_id}.png"
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_file)
        
        payment_url = f"https://example.com/pay?{urlencode(payment_data)}"
        
        return PackageResponse(
            package=package,
            qr_file=qr_file,
            payment_url=payment_url
        )
