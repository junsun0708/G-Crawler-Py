import requests
import json
import os
from prettytable import PrettyTable

class MSITManager:
    def __init__(self, service_key):
        self.url = 'http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList'
        self.service_key = ''
        self.file_path = 'msit_data.json' # 데이터를 저장할 파일 이름
        self.all_data = []

    # [사용자님의 성공 로직]
    def find_items_recursive(self, obj):
        if isinstance(obj, dict):
            if 'items' in obj and isinstance(obj['items'], list):
                return obj['items']
            for v in obj.values():
                res = self.find_items_recursive(v)
                if res: return res
        elif isinstance(obj, list):
            for v in obj:
                res = self.find_items_recursive(v)
                if res: return res
        return []

    def get_total_count(self, obj):
        if isinstance(obj, dict):
            if 'totalCount' in obj: return obj['totalCount']
            for v in obj.values():
                res = self.get_total_count(v)
                if res: return res
        elif isinstance(obj, list):
            for v in obj:
                res = self.get_total_count(v)
                if res: return res
        return 0

    def sync_from_api(self):
        """API에서 전체 데이터를 긁어와 파일로 저장합니다."""
        print("🌐 API 서버에서 최신 데이터를 가져옵니다. (잠시만 기다려주세요)")
        temp_storage = []
        params = {
            'serviceKey': self.service_key,
            'pageNo': '1',
            'numOfRows': '100',
            'returnType': 'json'
        }

        try:
            res = requests.get(self.url, params=params)
            data = res.json()
            total_count = int(self.get_total_count(data) or 0)

            if total_count == 0:
                print("❌ 데이터를 가져올 수 없습니다. 키를 확인하세요.")
                return

            total_pages = (total_count // 100) + 1
            for page in range(1, total_pages + 1):
                params['pageNo'] = str(page)
                res = requests.get(self.url, params=params)
                items = self.find_items_recursive(res.json())
                
                for entry in items:
                    item = entry.get('item', {}) if isinstance(entry, dict) else {}
                    if item: temp_storage.append(item)
                
                print(f"📥 수집 중: {len(temp_storage)} / {total_count}", end='\r')

            # 파일로 저장
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(temp_storage, f, ensure_ascii=False, indent=4)
            
            self.all_data = temp_storage
            print(f"\n✅ 동기화 완료! '{self.file_path}'에 저장되었습니다.")

        except Exception as e:
            print(f"\n❌ 동기화 에러: {e}")

    def load_data(self):
        """저장된 파일에서 데이터를 읽어옵니다. 파일이 없으면 동기화를 시도합니다."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.all_data = json.load(f)
            print(f"📂 로컬 파일에서 {len(self.all_data)}건의 데이터를 로드했습니다.")
        else:
            print("💡 저장된 데이터가 없습니다.")
            self.sync_from_api()

    def search(self, keyword):
        """메모리에 로드된 데이터에서 검색"""
        table = PrettyTable()
        table.field_names = ["No", "게시일", "담당부서", "제목"]
        table.align["제목"] = "l"
        table.max_width["제목"] = 50

        count = 0
        for item in self.all_data:
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

# --- 실행 ---
if __name__ == "__main__":
    MY_KEY = '여러분의_서비스키'
    msit = MSITManager(MY_KEY)

    # 1. 일단 로컬 파일에서 불러오기 (API 호출 안 함)
    msit.load_data()

    while True:
        print("\n" + "="*60)
        print("1. 검색 | 2. 데이터 최신 업데이트(API동기화) | q. 종료")
        menu = input("👉 선택: ").strip()

        if menu == '1':
            query = input("🔍 검색어 입력 (예: AI, 바이오): ").strip()
            msit.search(query)
        elif menu == '2':
            msit.sync_from_api()
        elif menu == 'q':
            break

