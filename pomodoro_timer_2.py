import time

print("分単位で設定できるポモドーロタイマー")

sets_input = input("何セット繰り返しますか？（数字）:")
max_sets = int(sets_input)

work_min_input = input("1セットの作業時間は何分ですか？（数字）:")
work_seconds = int(work_min_input) * 60

break_min_input = input("休憩時間は何分ですか？（数字）:")
break_seconds = int(break_min_input) * 60

current_set = 1

while current_set <= max_sets:
    print(f"\n--- 【 {current_set} / {max_sets} セット 】 ---")
    w_sec = work_seconds
    print(f"集中タイム ({work_min_input}分 / {w_sec}秒) スタート")

    while w_sec > 0:
        print(w_sec)
        time.sleep(1)
        w_sec = w_sec - 1

    print("作業終了、お疲れ様でした")

    b_sec = break_seconds
    print(f"休憩タイム ({break_min_input}分 / {b_sec}秒) スタート")

    while b_sec > 0:
        print(b_sec)
        time.sleep(1)
        b_sec = b_sec - 1

    print(f"{current_set}セット終了")
    current_set = current_set + 1

print("\n全セット終了、お疲れ様でした")    