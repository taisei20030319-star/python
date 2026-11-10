import time

# タイマーの秒数を設定（テスト用に１０秒）
seconds=10

print("start")

#秒数が０より大きい間、ずっと繰り返す
while seconds > 0:
    print(seconds)
    time.sleep(1) #１秒待つ
    seconds = seconds - 1 #秒数を１減らす

print("時間になりました！お疲れ様でした！")