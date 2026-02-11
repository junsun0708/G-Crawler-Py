import requests
from prettytable import PrettyTable

def get_msit_all_data():
    url = 'http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList'
    
    # 1. 서비스키 입력
    service_key = '' 

    all_collected_items = []
    
    # 2. 첫 호출 (전체 개수를 파악하기 위해 한 번 가져옴)
    try:
        print("🔄 데이터 동기화 중... (전체 목록을 불러오고 있습니다)")
        params = {
            'serviceKey': service_key,
            'pageNo': '1',
            'numOfRows': '100',
            'returnType': 'json'
        }
        response = requests.get(url, params=params)
        data = response.json()

        # [사용자님의 성공 로직 그대로 적용 - totalCount 찾기용]
        def get_total_count(obj):
            if isinstance(obj, dict):
                if 'totalCount' in obj: return obj['totalCount']
                for v in obj.values():
                    res = get_total_count(v)
                    if res: return res
            elif isinstance(obj, list):
                for v in obj:
                    res = get_total_count(v)
                    if res: return res
            return None

        total_count = int(get_total_count(data) or 0)
        if total_count == 0:
            print("❌ 데이터를 가져올 수 없습니다. API 키를 확인하세요.")
            return

        total_pages = (total_count // 100) + 1
        
        # 3. 전체 페이지 돌면서 데이터 수집
        for page in range(1, total_pages + 1):
            params['pageNo'] = str(page)
            res = requests.get(url, params=params)
            current_data = res.json()

            # --- 사용자님이 주신 성공 로직 그대로 시작 ---
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
            
            find_items(current_data)
            # --- 사용자님이 주신 성공 로직 그대로 끝 ---

            for entry in real_items:
                item = entry.get('item', {}) if isinstance(entry, dict) else {}
                if item:
                    all_collected_items.append(item)
            
            print(f"📥 수집 중: {len(all_collected_items)} / {total_count}", end='\r')

        print(f"\n✅ 동기화 완료! 총 {len(all_collected_items)}건 로드되었습니다.")

        # 4. 수집된 전체 데이터에서 검색 (태그/키워드)
        while True:
            print("\n" + "="*60)
            search_keyword = input("🔍 검색할 키워드나 태그(#)를 입력하세요 (종료: q): ").strip()
            if search_keyword.lower() == 'q': break
            
            keyword = search_keyword.replace('#', '')

            table = PrettyTable()
            table.field_names = ["No", "게시일", "담당부서", "제목"]
            table.align["제목"] = "l"
            table.max_width["제목"] = 50

            count = 0
            for item in all_collected_items:
                subject = item.get('subject', '')
                dept = item.get('deptName', '')
                
                if keyword in subject or keyword in dept:
                    count += 1
                    table.add_row([count, item.get('pressDt', '-'), dept, subject])

            if count > 0:
                print(table)
                print(f"✅ '{keyword}' 검색 결과: {count}건")
            else:
                print(f"❌ '{keyword}'와 일치하는 결과가 없습니다.")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    get_msit_all_data()