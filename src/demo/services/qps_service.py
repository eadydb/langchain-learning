"""QPS服务模块"""
from datetime import datetime, timedelta
from typing import List
import random
import numpy as np
from ..models.qps import QPSData, QPSResponse

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
        # 获取当前小时
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
        计算指定时间窗口内的QPS数据
        
        Args:
            time_window_minutes: 需要查看的时间窗口（分钟）
            data_points: 返回的数据点数量
            
        Returns:
            QPSResponse: 包含QPS数据的响应对象
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=time_window_minutes)
        
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
            message="QPS数据获取成功",
            data=qps_data
        )
