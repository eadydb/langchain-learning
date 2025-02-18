"""Main application module."""
import json
from typing import Dict, Any, Optional, List, Tuple
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from .services.calculator_service import CalculatorService
from .services.order_service import OrderService
from .services.package_service import PackageService
from .services.qps_service import QPSService
from .services.weather_service import WeatherService
from .utils.helpers import extract_json_from_response
from .schemas.base import (
    WeatherResponse,
    CalculationResponse,
    OrderResponse,
    PackageResponse,
    QPSResponse
)

import time
import redis
from datetime import datetime, timedelta
import numpy as np

def calculate_qps(time_window_minutes: int = 5, data_points: int = 10) -> List[Tuple[datetime, float]]:
    """
    Calculate QPS (Queries Per Second) for the last N minutes.
    
    Args:
        time_window_minutes: Number of minutes to look back
        data_points: Number of data points to return
    
    Returns:
        List of tuples containing timestamp and QPS value
    """
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=time_window_minutes)
    
    # Convert to timestamps
    end_ts = int(end_time.timestamp())
    start_ts = int(start_time.timestamp())
    
    # Get counts from Redis
    counts = redis_client.zrangebyscore('request_log', start_ts, end_ts, withscores=True)
    
    if not counts:
        return [(datetime.fromtimestamp(start_ts + i * (end_ts - start_ts) / data_points), 0.0) 
                for i in range(data_points)]
    
    # Create time windows
    window_size = (end_ts - start_ts) / data_points
    windows = [(start_ts + i * window_size, start_ts + (i + 1) * window_size) 
              for i in range(data_points)]
    
    # Calculate QPS for each window
    result = []
    for window_start, window_end in windows:
        window_counts = [count for _, count in counts 
                        if window_start <= count < window_end]
        qps = len(window_counts) / window_size
        result.append((datetime.fromtimestamp(window_start), qps))
    
    return result

def format_qps_response(qps_data: List[Tuple[datetime, float]]) -> Dict[str, Any]:
    """Format QPS data into standard response structure."""
    return {
        "status": "success",
        "data": {
            "timestamps": [ts.strftime('%Y-%m-%d %H:%M:%S') for ts, _ in qps_data],
            "qps_values": [round(qps, 2) for _, qps in qps_data]
        },
        "message": "QPS数据获取成功"
    }

def record_request():
    """Record a request in Redis with current timestamp"""
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    current_ts = int(time.time())
    redis_client.zadd('request_log', {str(current_ts): current_ts})
    
    # Clean old data (keep only last 10 minutes)
    old_ts = current_ts - 600  # 10 minutes
    redis_client.zremrangebyscore('request_log', 0, old_ts)

# Define function schemas
FUNCTIONS = [
    {
        "name": "get_current_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市名称，如：Beijing, Shanghai"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "calculator",
        "description": "执行基本的数学运算",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "number",
                    "description": "第一个数"
                },
                "y": {
                    "type": "number",
                    "description": "第二个数"
                },
                "operation": {
                    "type": "string",
                    "enum": ["加", "减", "乘", "除"],
                    "description": "运算类型"
                }
            },
            "required": ["x", "y", "operation"]
        }
    },
    {
        "name": "get_recent_orders",
        "description": "获取用户最近的订单信息",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "用户ID"
                }
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "create_custom_package",
        "description": "创建自定义套餐",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "套餐名称"
                },
                "duration": {
                    "type": "integer",
                    "description": "套餐时长（月）"
                },
                "features": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "套餐包含的功能列表"
                },
                "price": {
                    "type": "number",
                    "description": "套餐价格"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "calculate_qps",
        "description": "计算最近一段时间的QPS数据",
        "parameters": {
            "type": "object",
            "properties": {
                "time_window_minutes": {
                    "type": "integer",
                    "description": "时间窗口（分钟）"
                },
                "data_points": {
                    "type": "integer",
                    "description": "返回的数据点数量",
                    "default": 10
                }
            },
            "required": ["time_window_minutes"]
        }
    }
]


class FunctionCallingDemo:
    """Main application class for the function calling demo."""
    
    def __init__(self):
        """Initialize the demo application."""
        self.llm = Ollama(
            model="qwen2.5-coder:32b",
            base_url="http://192.168.0.16:11434",
            callbacks=[StreamingStdOutCallbackHandler()],
            temperature=0
        )
        self.weather_service = WeatherService()
        self.calculator_service = CalculatorService()
        self.order_service = OrderService()
        self.package_service = PackageService()
        self.qps_service = QPSService()
    
    def process_query(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Process a user query and execute the appropriate function.
        
        Args:
            query: User input query.
            
        Returns:
            Function result or None if query couldn't be processed.
        """
        print("\n正在思考...")
        
        # Generate response with function calling capability
        response = self.llm.invoke(
            f"""你是一个函数调用助手。根据用户的请求，判断是否需要调用函数。

用户请求: "{query}"

可用的函数:
{json.dumps(FUNCTIONS, indent=2, ensure_ascii=False)}

如果需要调用函数，请直接返回一个JSON对象，格式如下：
{{
    "function": "函数名称",
    "parameters": {{
        "参数1": "值1",
        ...
    }}
}}

注意：
1. 只输出JSON对象，不要有任何其他解释文字
2. 如果不需要调用函数，返回空的JSON对象 {{}}
3. 对于自定义套餐，从用户输入中提取：
   - 套餐名称（必须）
   - 时长（如果提到）
   - 功能列表（如果提到）
   - 价格（如果提到）
"""
        )
        
        # Extract and process function call
        function_call = extract_json_from_response(response)
        if function_call and "function" in function_call and function_call["function"]:
            return self._execute_function(function_call)
        return None
    
    def _execute_function(self, function_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the specified function with given parameters.
        
        Args:
            function_call: Dictionary containing function name and parameters.
            
        Returns:
            Function result.
            
        Raises:
            ValueError: If function is not recognized.
        """
        function_name = function_call["function"]
        parameters = function_call["parameters"]
        
        if function_name == "get_current_weather":
            return self.weather_service.get_current_weather(**parameters)
        elif function_name == "calculator":
            return self.calculator_service.calculate(**parameters)
        elif function_name == "get_recent_orders":
            return self.order_service.get_recent_orders(**parameters)
        elif function_name == "create_custom_package":
            return self.package_service.create_custom_package(**parameters)
        elif function_name == "calculate_qps":
            result = self.qps_service.calculate_qps(**parameters)
            print("\nQPS统计结果:")
            print(f"状态: {result.status}")
            print(f"消息: {result.message}")
            print("\n时间点数据:")
            for point in result.data:
                print(f"时间: {point.timestamp.strftime('%Y-%m-%d %H:%M:%S')}, QPS: {point.qps_value:.2f}")
            return result
        else:
            raise ValueError(f"Unknown function: {function_name}")
    
    def print_result(self, result: Dict[str, Any]):
        """
        Print function result in a formatted way.
        
        Args:
            result: Function result to print.
        """
        if isinstance(result, WeatherResponse):
            print("查询结果:")
            print(f"城市: {result.location}")
            print(f"温度: {result.temperature}°{result.unit}")
            print(f"天气: {', '.join(result.forecast)}")
            
        elif isinstance(result, CalculationResponse):
            print("计算结果:")
            print(f"{result.x} {result.operation} {result.y} = {result.result}")
            
        elif isinstance(result, OrderResponse):
            print(f"{result.user_id} 的订单查询结果:")
            print(f"查询期间: {result.period}")
            print(f"订单总数: {result.total_orders}")
            print("\n订单详情:")
            print("-" * 80)
            print(f"{'订单号':<15} {'日期':<30} {'商品':<15} {'数量':<10} {'单价':<10} {'总价':<10} {'状态':<10}")
            print("-" * 80)
            for order in result.orders:
                print(f"{order.order_id:<15} {order.date:<30} {order.product:<15} {order.quantity:<10} {order.price:<10.1f} {order.total:<10.1f} {order.status:<10}")
            print("-" * 80)
            
        elif isinstance(result, PackageResponse):
            print("自定义套餐创建成功!")
            print(f"套餐名称: {result.package.name}")
            print(f"套餐ID: {result.package.id}")
            print(f"时长: {result.package.duration}")
            print(f"价格: {result.package.price}元")
            print("\n包含功能:")
            for feature in result.package.features:
                print(f"- {feature}")
            print(f"\n二维码已生成: {result.qr_file}")
            print(f"支付链接: {result.payment_url}")
            
        elif isinstance(result, QPSResponse):
            print("\nQPS统计结果:")
            print(f"状态: {result.status}")
            print(f"消息: {result.message}")
            print("\n时间点数据:")
            for point in result.data:
                print(f"时间: {point.timestamp.strftime('%Y-%m-%d %H:%M:%S')}, QPS: {point.qps_value:.2f}")
    
    def print_qps_result(self, result: Dict[str, Any]):
        """
        Print QPS result in a formatted way.
        
        Args:
            result: QPS result to print.
        """
        print("\nQPS统计结果:")
        print(f"状态: {result.status}")
        print(f"消息: {result.message}")
        print("\n时间点数据:")
        for point in result.data:
            print(f"时间: {point.timestamp.strftime('%Y-%m-%d %H:%M:%S')}, QPS: {point.qps_value:.2f}")


def main():
    """Main function to run the demo."""
    demo = FunctionCallingDemo()
    
    print("\n欢迎使用 Function Calling Demo!")
    print("你可以问我：")
    print("1. 天气相关：'北京的天气怎么样？'")
    print("2. 计算相关：'帮我计算23乘以45'")
    print("3. 订单查询：'查询用户12345最近3个月的订单'")
    print("4. 套餐定制：'创建3个月的高级套餐，包含数据分析和专家咨询功能'")
    print("5. QPS计算：'计算最近5分钟的QPS'")
    print("输入 'q' 退出\n")
    
    while True:
        query = input("\n请输入你的问题: ")
        
        if query.lower() == 'q':
            print("谢谢使用，再见！")
            break
        
        try:
            result = demo.process_query(query)
            if result:
                demo.print_result(result)
            else:
                print("\n无法理解你的问题，请尝试换个方式提问。")
                print("例如：")
                print("- '上海的天气如何？'")
                print("- '计算 15 加 27'")
                print("- '查询用户U123的订单'")
                print("- '创建一个包含数据分析的6个月高级套餐'")
                print("- '计算最近5分钟的QPS'")
        except Exception as e:
            print(f"\n处理请求时出错: {str(e)}")


if __name__ == "__main__":
    main()
