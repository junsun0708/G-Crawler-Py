import requests
from prettytable import PrettyTable

def get_gov_announcement():
    url = 'http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList'
    
    # 1. 서비스키 입력 (작동하는 키를 넣어주세요)
    service_key = '' 

    # 키워드 입력 받기
    search_keyword = input("🔍 검색할 키워드를 입력하세요 (전체는 엔터): ").strip()

    params = {
        'serviceKey': service_key,
        'pageNo': '1',
        'numOfRows': '20',  # 넉넉하게 20건 가져옴
        'returnType': 'json'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # [핵심] 진짜 'items' 리스트를 찾을 때까지 파고드는 로직
        real_items = []
        def find_items(obj):
            nonlocal real_items
            if isinstance(obj, dict):
                if 'items' in obj and isinstance(obj['items'], list):
                    real_items = obj['items']
                    return
                for v in obj.values():
                    find_items(v)
                    if real_items: return
            elif isinstance(obj, list):
                for v in obj:
                    find_items(v)
                    if real_items: return

        find_items(data)

        if not real_items:
            print("🔔 공고 데이터를 찾을 수 없습니다.")
            return

        # 표 설정 (이미지 상세 항목 반영)
        table = PrettyTable()
        table.field_names = ["No", "게시일", "담당부서", "제목", "담당자", "연락처"]
        table.align["제목"] = "l"
        table.max_width["제목"] = 40

        count = 0
        for entry in real_items:
            # {'item': {...}} 구조에서 알맹이 꺼내기
            item = entry.get('item', {}) if isinstance(entry, dict) else {}
            
            subject = item.get('subject', '')
            dept = item.get('deptName', '')

            # 필터링 조건 (키워드가 제목이나 부서에 포함될 때)
            if search_keyword in subject or search_keyword in dept:
                count += 1
                table.add_row([
                    count,
                    item.get('pressDt', '-'),
                    dept,
                    subject,
                    item.get('managerName', '-'),
                    item.get('managerTel', '-')
                ])

        print(table)
        print(f"\n✅ 검색 결과: 총 {count}건 표시 중 (전체 {len(real_items)}건 중)")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    get_gov_announcement()