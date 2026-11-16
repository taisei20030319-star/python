import streamlit as st
import pandas as pd

#ページのレイアウト設定
st.set_page_config(page_title="麻雀ポイント計算アプリ", page_icon="🀄️", layout="centered")

st.title("🀄️ 麻雀 持ち点・ポイント計算アプリ")
st.write("ゲーム終了時の持ち点を入れるだけで、ウマ・オカを自動計算して収支を出します")

#---設定エリア---
st.subheader("⚙️ ルール設定")
col_s1, col_s2=st.columns(2)
with col_s1:
     starting_score=st.number_input("持ち点（例：25000) ", value=25000, step=1000)
with col_s2:
     return_score=st.number_input("返し点・基準点（例：30000）", value=30000, step=1000)

#ウマの設定（1位〜4位）
st.write("---")
st.write("**ウマの設定 (ex: 10-20 なら 20,10,-10,-20)**")
col_u1, col_u2, col_u3, col_u4=st.columns(4)
with col_u1:
     uma_1=st.number_input("1位 ウマ", value=20)
with col_u2:
     uma_2=st.number_input("2位 ウマ", value=10)
with col_u3:
     uma_3=st.number_input("3位 ウマ", value=-10)
with col_u4:
     uma_4=st.number_input("4位 ウマ", value=-20)

rate=st.number_input("レート (ex: 50 = 1000点50円 / 1 = 1P 1円)", value=50, step=10)

#---プレイヤーの名前と点数入力エリア---
st.write("---")
st.subheader("👥 プレイヤーの最終持ち点入力")
expected_total=starting_score*4
st.info("※4人の点数の合計が、配給原点（{expexted_total:,}点）と一致しているか確認してください")

col_p1, col_p2=st.columns(2)
with col_p1:
     p1_name=st.text_input("プレイヤー1の名前", value="プレイヤーA")
     p1_score=st.number_input(f"{p1_name}の持ち点", value=35000, step=100)

     p2_name=st.text_input("プレイヤー2の名前", value="プレイヤーB")
     p2_score=st.number_input(f"{p2_name}の持ち点", value=30000, step=100)

with col_p2:
     p3_name=st.text_input("プレイヤー3の名前", value="プレイヤーC")
     p3_score=st.number_input(f"{p1_name}の持ち点", value=20000, step=100)
     
     p4_name=st.text_input("プレイヤー4の名前", value="プレイヤーD")
     p4_score=st.number_input(f"{p2_name}の持ち点", value=15000, step=100)

#点数の合計チェック
total_score=p1_score+p2_score+p3_score+p4_score
st.write(f"現在の点数合計: **{total_score:,}点 **（基準:{expected_total:,}点)")

if total_score !=expected_total:
     st.warning(f"⚠️ 点数の合計が合っていません (差分:{total_score - expected_total:,}点)。入力値を確認してください")

# ---計算ボタン---
if st.button("🧮 ポイントを計算する", use_container_width=True):
     #データをまとめて順位（高い順）に並び替える
     players=[
          {"name":p1_name, "score": p1_score},
          {"name":p2_name, "score": p2_score},
          {"name":p3_name, "score": p3_score},
          {"name":p4_name, "score": p4_score},
     ]

     #持ち点が高い順にソートする
     players_sorted=sorted(players, key=lambda x: x["score"], reverse=True)
     umas=[uma_1, uma_2, uma_3, uma_4]

     results=[]
     for rank, p in enumerate(players_sorted):
          #1.素点の計算（返し点基準。ex: (35000-30000)/1000=+5pt)
          soten=(p["score"]-return_score)/1000

          #ウマを足す
          uma=umas[rank]
          total_point=soten+uma

          results.append({
               "順位": f"{rank+1}位",
               "名前": p["name"],
               "持ち点": f"{p['score']:,}点",
               "素点pt": round(soten, 1),
               "トータルpt": round(total_point, 1)
          })
    #表にして表示
     df=pd.DataFrame(results)
     st.success("ポイント計算が完了しました")
     st.dataframe(df, use_container_width=True)