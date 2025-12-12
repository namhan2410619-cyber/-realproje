import streamlit as st
from agents.data_agent import get_weather, get_traffic, get_bus_arrival
from agents.route_agent import get_route
from agents.schedule_agent import calc_wake_time
from agents.iot_agent import send_alarm
from utils.map_utils import display_route_map

st.set_page_config(page_title="SmartCommute", layout="wide")

st.title("🏫 SmartCommute Assistant")
st.write("등교 시간 기반 최적 경로 및 기상 알람 시스템")

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🗺 현재 위치 입력")
    start_lat = st.number_input("현재 위도", value=37.5665)
    start_lng = st.number_input("현재 경도", value=126.9780)

with col2:
    st.subheader("🎯 목적지 위치 입력")
    end_lat = st.number_input("학교 위도", value=37.4500)
    end_lng = st.number_input("학교 경도", value=126.9500)

st.subheader("⏰ 설정")
school_time = st.time_input("등교 시간", value=None)
prep_time = st.number_input("준비 시간(분)", value=40)

if st.button("최적 경로 계산 실행"):
    st.write("### 🔍 데이터를 수집 중...")

    weather = get_weather()
    traffic = get_traffic(start_lat, start_lng, end_lat, end_lng)
    bus_info = get_bus_arrival()

    st.write("### 🌦 날씨:", weather)
    st.write("### 🚗 교통 상황:", traffic)
    st.write("### 🚌 버스 도착 정보:", bus_info)

    route = get_route((start_lat, start_lng), (end_lat, end_lng))

    st.write(f"### ⏳ 예상 이동 시간: **{route['duration_min']} 분**")

    wake_time = calc_wake_time(
        school_time,
        prep_time,
        route["duration_min"],
        weather
    )

    st.success(f"⏰ 추천 기상시간: **{wake_time}**")

    # 지도 표시
    st.write("### 🗺 최적 경로 지도")
    display_route_map(route["path"], (start_lat, start_lng), (end_lat, end_lng))

    # IoT 전송
    if st.button("IoT 알람으로 전송"):
        send_alarm(str(wake_time))
        st.success("IoT 알람 전송 완료!")
