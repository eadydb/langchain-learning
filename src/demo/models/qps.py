"""QPS数据模型模块"""
from datetime import datetime
from typing import List
from dataclasses import dataclass

@dataclass
class QPSData:
    """单个QPS数据点的模型"""
    timestamp: datetime
    qps_value: float

@dataclass
class QPSResponse:
    """QPS响应数据的模型"""
    status: str
    message: str
    data: List[QPSData]
