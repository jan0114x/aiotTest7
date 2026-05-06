import urllib.request                                   # 웹 요청 라이브러리
import json                                             # JSON 데이터 처리 라이브러리
import datetime                                         # 날짜 및 시간 라이브러리
import asyncio                                          # 비동기 실행 라이브러리
from telegram import Bot                                # 텔레그램 봇 객체 가져오기

telegram_id = '8424398005'                              # 내 텔레그램 채팅 ID
my_token = '8616454904:AAHi8Kn600HEHbJ3ptXEll6Ir41Gdof3jYg' # 봇 파더에서 발급받은 토큰
api_key = 'cc37b0614c9981813b5fd8efb1d84684'            # 오픈웨더맵 API 키
bot = Bot(token=my_token)                               # 토큰으로 봇 객체 생성

ALERT_HOURS = [7, 10, 13, 16, 19, 22]                   # 3시간 간격 정각 알림 시간 목록
ALERT_TIMES = ["11:26", "14:45"]                        # 사용자가 추가 지정한 알림 시간

def getWeather():                                       # 날씨 정보를 가져와 문자열로 반환하는 함수
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8" # 서울 예보 요청 URL
    with urllib.request.urlopen(url) as r:              # API 서버에 요청 보내기
        data = json.loads(r.read())                     # 받은 응답을 JSON 형식으로 변환
        text = ""                                       # 결과 저장용 문자열 초기화
        for i in range(8):                              # 24시간을 3시간 단위로 나눈 8개 슬롯 반복
            item = data['list'][i]                      # 현재 순서의 날씨 데이터 추출
            hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2) # KST 한국 시간으로 변환
            temp = item['main']['temp']                 # 현재 기온 정보 추출
            humi = item['main']['humidity']             # 현재 습도 정보 추출
            desc = item['weather'][0]['description']    # 날씨 상태 설명 추출
            text += f"({hour}시 {temp}도 {humi}% {desc})\n" # 형식에 맞춰 문자열 생성
        return text                                     # 최종 날씨 문자열 반환

async def main():                                       # 비동기 실행을 위한 메인 함수
    try:                                                # 오류 발생을 대비한 예외 처리 시작
        while True:                                     # 프로그램 종료 전까지 무한 반복
            now = datetime.datetime.now()               # 현재 시스템 시간 가져오기
            hm = now.strftime('%H:%M')                  # 현재 시와 분만 추출
            
            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0 # 정각 알림 조건 확인
            is_alert_time = hm in ALERT_TIMES and now.second == 0 # 특정 지정 시간 알림 조건 확인
            
            if is_alert_hour or is_alert_time:          # 위 두 조건 중 하나라도 만족할 경우
                msg = getWeather()                      # 날씨 함수 호출하여 메시지 생성
                print(msg)                              # 터미널 창에 결과 출력
                await bot.send_message(chat_id=telegram_id, text=msg) # 텔레그램 봇으로 메시지 발송
            
            await asyncio.sleep(1)                      # 1초 동안 대기 후 다음 루프 실행
    except KeyboardInterrupt:                           # 사용자가 Ctrl+C를 눌러 종료했을 때
        pass                                            # 아무 문제 없이 프로그램을 종료함

if __name__ == "__main__":                              # 스크립트가 직접 실행될 경우
    asyncio.run(main())                                 # 비동기 메인 함수 실행
