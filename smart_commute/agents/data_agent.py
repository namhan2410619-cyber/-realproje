import requests
from utils.api_keys import WEATHER_KEY, TRAFFIC_KEY

### 1) 날씨 정보 (기상청 단기예보)
def get_weather():
    # Demo: 실제 API로 변경 가능
    return "맑음"

### 2) 교통 정보
def get_traffic(start_lat, start_lng, end_lat, end_lng):
    # Demo 구현
    return "원활"

### 3) 버스/지하철 정보
def get_bus_arrival():
    return "5분 후 도착 예정"
