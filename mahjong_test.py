import streamlit as st
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

st.set_page_config(page_title="何切るテスト", layout="centered")
st.title("何切るテスト確認")

hand_input=st.text_input("手牌を14枚入力", value="2m 3m 4m 5p 6p 7p 1s 2s 3s 5s 6s 7s 9s 9s")

if st.button("計算する"):
    hand_14=[t.strip() for t in hand_input.split() if t.strip()]
    st.write(f"受け取った手牌リスト：{hand_14}")

    if len(hand_14)==14:
        try:
            oneline="".join(hand_14)
            arr=TilesConverter.one_line_string_to_34_array(oneline)
            shanten=Shanten()
            s=shanten.calculate_shanten(arr)
            st.success(f"計算成功 現在のシャンテン数：{s}")
        except Exception as e:
            st.error(f"エラーが発生しました：{e}")
    else:
        st.warning(f"枚数が14枚ではありません（現在 {len(hand_14)}枚）")