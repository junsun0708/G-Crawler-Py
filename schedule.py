"""
MSIT 공공 API 데이터 동기화 스케줄러
- 매일 1회(기본: 오전 3시) msit_sync_file.py의 sync_from_api()를 실행합니다.
- 실행 즉시 첫 동기화를 수행한 뒤, 이후 매일 지정 시각에 반복합니다.

사용법:
    python schedule.py                  # 기본(매일 03:00)
    python schedule.py --time 06:30     # 매일 06:30
    python schedule.py --now-only       # 즉시 1회만 실행 후 종료
"""

import argparse
import signal
import sys
import time
from datetime import datetime, timedelta

from msit_sync_file import MSITManager


def run_sync():
    """동기화 1회 실행"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}")
    print(f"⏰ [{now}] 동기화 작업을 시작합니다...")
    print(f"{'='*60}")

    try:
        msit = MSITManager(service_key="")  # 클래스 내부에 키가 하드코딩되어 있으므로 빈 값 전달
        msit.sync_from_api()
        print(f"✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 동기화 작업 완료!\n")
    except Exception as e:
        print(f"❌ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 동기화 실패: {e}\n")


def seconds_until(target_hour: int, target_minute: int) -> float:
    """다음 target_hour:target_minute 까지 남은 초를 반환"""
    now = datetime.now()
    target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


def main():
    parser = argparse.ArgumentParser(description="MSIT 공공 API 일일 동기화 스케줄러")
    parser.add_argument(
        "--time",
        type=str,
        default="03:00",
        help="매일 실행할 시각 (HH:MM 형식, 기본: 03:00)",
    )
    parser.add_argument(
        "--now-only",
        action="store_true",
        help="즉시 1회만 실행하고 종료",
    )
    args = parser.parse_args()

    # Ctrl+C 로 깔끔하게 종료
    def handle_signal(sig, frame):
        print("\n🛑 스케줄러를 종료합니다.")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # --now-only: 즉시 1회 실행 후 종료
    if args.now_only:
        run_sync()
        return

    # 시각 파싱
    try:
        hour, minute = map(int, args.time.split(":"))
        assert 0 <= hour <= 23 and 0 <= minute <= 59
    except (ValueError, AssertionError):
        print("❌ 시각 형식이 올바르지 않습니다. HH:MM 형식으로 입력하세요. (예: 03:00)")
        sys.exit(1)

    print(f"🚀 MSIT 동기화 스케줄러 시작!")
    print(f"📅 매일 {hour:02d}:{minute:02d} 에 자동 동기화됩니다.")
    print(f"🛑 종료하려면 Ctrl+C 를 누르세요.\n")

    # 시작 직후 첫 동기화 실행
    run_sync()

    # 매일 반복
    while True:
        wait = seconds_until(hour, minute)
        next_run = datetime.now() + timedelta(seconds=wait)
        print(f"💤 다음 실행 예정: {next_run.strftime('%Y-%m-%d %H:%M:%S')} ({wait/3600:.1f}시간 후)")

        time.sleep(wait)
        run_sync()


if __name__ == "__main__":
    main()
