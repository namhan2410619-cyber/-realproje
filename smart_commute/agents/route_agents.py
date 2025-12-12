import requests
from utils.api_keys import NAVER_ID, NAVER_SECRET

def get_route(start, end):
    url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_ID,
        "X-NCP-APIGW-API-KEY": NAVER_SECRET
    }
    params = {
        "start": f"{start[1]},{start[0]}",
        "goal": f"{end[1]},{end[0]}"
    }

    res = requests.get(url, headers=headers, params=params).json()
    route = res["route"]["traoptimal"][0]

    return {
        "duration_min": route["summary"]["duration"] / 1000 / 60,
        "path": route["path"],
    }
