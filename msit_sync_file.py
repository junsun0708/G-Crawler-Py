import requests
import json
import os
import time

class MSITManager:
    def __init__(self, service_key):
        self.url = 'http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList'
        self.service_key = service_key
        self.file_path = 'msit_data.json'
        self.all_data = []

    def find_items_recursive(self, obj):
        items_found = []
        if isinstance(obj, dict):
            # 'items' 키 내부를 샅샅이 뒤짐
            if 'items' in obj and isinstance(obj['items'], list):
                for entry in obj['items']:
                    item = entry.get('item') if isinstance(entry, dict) and 'item' in entry else entry
                    if isinstance(item, dict):
                        items_found.append(item)
            for v in obj.values():
                items_found.extend(self.find_items_recursive(v))
        elif isinstance(obj, list):
            for v in obj:
                items_found.extend(self.find_items_recursive(v))
        return items_found

    def get_total_count(self, obj):
        if isinstance(obj, dict):
            if 'totalCount' in obj: return int(obj['totalCount'])
            for v in obj.values():
                res = self.get_total_count(v)
                if res: return res
        elif isinstance(obj, list):
            for v in obj:
                res = self.get_total_count(v)
                if res: return res
        return 0

    def sync_from_api(self):
        print("\n🌐 API 서버에서 전체 데이터를 동기화합니다...")
        temp_storage = []
        
        # 안전을 위해 한 번에 100개씩 요청 (서버가 무시할 경우를 대비)
        params = {
            'serviceKey': self.service_key,
            'pageNo': '1',
            'numOfRows': '100', 
            'returnType': 'json'
        }

        try:
            # 1. 전체 개수 확인
            response = requests.get(self.url, params=params, timeout=15)
            first_data = response.json()
            total_count = self.get_total_count(first_data)

            if total_count == 0:
                print("❌ 데이터를 찾을 수 없습니다.")
                return

### 수정된 부분 시작 ###
            # 서버가 10개씩 줄 경우를 대비해 total_pages를 10으로 나누어 넉넉하게 잡습니다.
            total_pages = (total_count // 10) + 1 
            print(f"📊 총 {total_count}건 / 모든 데이터를 위해 약 {total_pages}페이지 탐색을 시작합니다.")

            # 2. 루프 돌며 누적 수집
            for page in range(1, total_pages + 1):
            ### 수정된 부분 끝 ###
                params['pageNo'] = str(page)
                
                found_in_this_page = False # 이번 페이지에서 데이터를 찾았는지 체크
                for attempt in range(3): 
                    try:
                        res = requests.get(self.url, params=params, timeout=15)
                        data = res.json()
                        page_items = self.find_items_recursive(data)
                        
                        if page_items:
                            temp_storage.extend(page_items)
                            found_in_this_page = True
                        break
                    except:
                        time.sleep(1)
                
                # 중복 제거를 포함한 현재 실시간 수집량 계산
                unique_dict = {item.get('subject'): item for item in temp_storage if item.get('subject')}
                current_unique = len(unique_dict)
                
                print(f"📥 수집 중: {current_unique} / {total_count} (진행: {page}p)", end='\r')
                
                # 데이터가 더 이상 안 나오거나 목표치에 도달하면 종료
                if not found_in_this_page and page > 40: # 최소 40페이지는 넘기고 판단
                    break
                if current_unique >= total_count:
                    break
                    
                time.sleep(0.1) # 속도를 조금 높였습니다.

            # 3. 최종 저장
            self.all_data = list(unique_dict.values())

            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.all_data, f, ensure_ascii=False, indent=4)
            
            print(f"\n✅ 동기화 완료! 총 {len(self.all_data)}건을 파일에 저장했습니다.")

        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            
    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.all_data = json.load(f)
            print(f"📂 로컬 파일 로드 완료: {len(self.all_data)}건")
        else:
            self.sync_from_api()

# ... (search 함수는 이전과 동일)

    def search(self, keyword):
        if not self.all_data:
            print("❌ 로드된 데이터가 없습니다. 업데이트를 먼저 진행하세요.")
            return
        table = PrettyTable()
        table.field_names = ["No", "게시일", "담당부서", "제목"]
        table.align["제목"] = "l"
        table.max_width["제목"] = 50
        
        count = 0
        for item in self.all_data:
            if keyword in item.get('subject', '') or keyword in item.get('deptName', ''):
                count += 1
                table.add_row([count, item.get('pressDt', '-'), item.get('deptName', '-'), item.get('subject', '-')])
        
        print(table)
        print(f"🔍 '{keyword}' 검색 결과: {count}건")

if __name__ == "__main__":
    MY_KEY = 'f64d660e3ef5d8283451c3c040d14405acbd6a7cea2d26cbcd28b5443bebb23c'
    msit = MSITManager(MY_KEY)
    msit.load_data()
    
    while True:
        print("\n" + "="*50)
        menu = input("1.검색 | 2.업데이트 | q.종료 : ").strip()
        if menu == '1':
            msit.search(input("검색어: "))
        elif menu == '2':
            msit.sync_from_api()
        elif menu == 'q':
            break