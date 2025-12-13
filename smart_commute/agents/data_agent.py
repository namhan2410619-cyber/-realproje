import requests
import datetime
from utils.api_keys import WEATHER_KEY
from utils.grid_convert import convert_to_grid

# 1) 기상청 단기예보 조회
def get_weather(lat, lng):
    nx, ny = convert_to_grid(lat, lng)

    now = datetime.datetime.now()
    base_date = now.strftime("%Y%m%d")

    # 단기예보는 30분 이전 발표된 시간 기준 필요
    hour = now.hour
    if now.minute < 30:
        hour -= 1
    base_time = f"{hour:02d}00"

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

    params = {
        "serviceKey": WEATHER_KEY,
        "numOfRows": 50,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }

    res = requests.get(url, params=params).json()

    items = res["response"]["body"]["items"]["item"]

    weather = {
        "rain": None,
        "sky": None,
        "temperature": None
    }

    for i in items:
        if i["category"] == "PTY":  # 강수형태
            weather["rain"] = i["fcstValue"]
        elif i["category"] == "SKY":
            weather["sky"] = i["fcstValue"]
        elif i["category"] == "T1H":
            weather["temperature"] = i["fcstValue"]

    # 설명 변환
    rain_map = {"0": "없음", "1": "비", "2": "비/눈", "3": "눈", "5": "빗방울", "6": "빗방울눈", "7": "눈날림"}
    sky_map = {"1": "맑음", "3": "구름많음", "4": "흐림"}

    return {
        "weather": sky_map.get(weather["sky"], "정보없음"),
        "rain": rain_map.get(weather["rain"], "정보없음"),
        "temp": weather["temperature"]
    }
