import requests
from prettytable import PrettyTable

def get_gov_announcement():
    url = 'http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList'
    
    # 1. 서비스키 입력
    service_key = '' 

    params = {
        'serviceKey': service_key,
        'pageNo': '1',
        'numOfRows': '10',
        'returnType': 'json'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # [핵심] 리스트 데이터를 찾을 때까지 안쪽으로 파고드는 로직
        target_list = []
        
        def find_list(obj):
            nonlocal target_list
            if isinstance(obj, list):
                target_list = obj
                return
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, list):
                        target_list = value
                        return
                    elif isinstance(value, dict):
                        find_list(value)
                        if target_list: return

        find_list(data)

        if not target_list:
            print("🔔 공고 데이터를 찾을 수 없습니다. API 응답을 확인해야 합니다.")
            print("응답 내용:", data)
            return

        # 2. 표 출력
        table = PrettyTable()
        table.field_names = ["No", "게시일", "담당부서", "제목"]
        table.align["제목"] = "l"
        table.max_width["제목"] = 50

        for i, item in enumerate(target_list, 1):
            print(f"DEBUG: 현재 아이템 내용 -> {item}")
            # item이 dict인지 확인 후 안전하게 추출
            if isinstance(item, dict):
                table.add_row([
                    i,
                    item.get('pressDt', '-'),
                    item.get('deptName', '-'),
                    item.get('subject', '-')
                ])
            else:
                # 데이터가 문자열 등으로 들어올 경우 대비
                table.add_row([i, "-", "-", str(item)])

        print(table)
        print(f"\n✅ 데이터 추출 성공: {len(target_list)}건 표시 중")

    except Exception as e:
        print(f"❌ 예상치 못한 에러: {e}")

if __name__ == "__main__":
    get_gov_announcement()