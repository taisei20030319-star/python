import time

user_input=input("何秒のタイマーを設定しますか？(数字を入力):")
seconds=int(user_input)
print(f"{seconds}秒のタイマースタート")
while seconds > 0:
    print(seconds)
    time.sleep(1)
    seconds=seconds-1