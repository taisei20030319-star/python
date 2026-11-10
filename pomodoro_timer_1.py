import time

print("ポモドーロタイマーを開始します")

max_sets = 3
current_set = 1

while current_set <= max_sets:
    print(f"\n--- 【{current_set} / {max_sets} セット】 ---")

    work_seconds = 5
    print(f"集中タイム{work_seconds}秒スタート ---")

    while work_seconds > 0:
        print(work_seconds)
        time.sleep(1)
        work_seconds=work_seconds - 1
    print("作業終了、お疲れ様でした")

    break_seconds = 3
    print(f"休憩時間{break_seconds}秒スタート ---")
    while break_seconds > 0:
        time.sleep(1)
        break_seconds = break_seconds - 1

    print(f"{current_set}セット終了")
    current_set = current_set + 1

print("\n全セット終了、お疲れ様でした")
