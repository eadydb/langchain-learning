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

