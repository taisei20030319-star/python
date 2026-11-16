import streamlit as st
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

#ページの設定
st.set_page_config(
    page_title="麻雀 牌効率・何切るチェッカー",
    page_icon="🀄️",
    layout="centered"
)

#全34種の牌リスト
ALL_TILES=[
    f"{i}{s}" for s in ["m", "p", "s"] for i in range(1, 10)
]+[f"{i}z" for i in range(1, 8)]

#牌の表示順やカテゴリ分け用のマッピング
SUITS={"m": "萬子", "p": "筒子", "s": "索子", "z": "字牌"}

def string_to_34_array(tile_str_list):
    """['1m', '2m', ...]を34要素の整数配列に変換"""
    oneline="".join(tile_str_list)
    return TilesConverter.one_line_string_to_34_array(oneline)

def count_remaining_deck(hand_14):
    """手牌14枚を除いた山に残っている牌の枚数"""
    deck={tile: 4 for tile in ALL_TILES}
    for tile in hand_14:
        if tile in deck:
            deck[tile]-=1
    return deck

def evaluate_nanikiru(hand_14):
    """何切る計算の実行"""
    shanten=Shanten()
    current_shanten=shanten.calculate_shanten(string_to_34_array(hand_14))

    unique_discards=list(set(hand_14))
    results={}
    deck=count_remaining_deck(hand_14)

    for discard in unique_discards:
        temp_hand=list(hand_14)
        temp_hand.remove(discard)
        base_13_shanten=shanten.calculate_shanten(string_to_34_array(temp_hand))

        effective_tiles=[]
        total_ukeire=0

        for tile, count in deck.items():
            if count<=0:
                continue
            test_hand=temp_hand+[tile]
            new_shanten=shanten.calculate_shanten(string_to_34_array(test_hand))

            #シャンテン数が進む、または有効な受け入れになる場合
            if new_shanten<base_13_shanten:
                effective_tiles.append((tile, count))
                total_ukeire+=count

        results[discard]={
            "total_ukeire": total_ukeire,
            "effective_tiles": effective_tiles,
            "shanten_after_discard": base_13_shanten
        }
    return current_shanten, sorted(
        results.items(),
        key=lambda x: x[1]["total_ukeire"],
        reverse=True
    )
#---UIデザインの構築---
st.title("🀄️ 麻雀 牌効率・何切るチェッカー")
st.write("14枚の手牌を入力（選択）すると、どの牌を切るのが一番受け入れ枚数が多いかを計算します。")

#入力フォーム:14枚の牌をスペース区切りで入力する方式
default_hand_str="2m 3m 4m 5p 6p 7p 1s 2s 3s 5s 6s 7s 9s 9s"
st.markdown("### 手牌の設定 (14枚)")
hand_input=st.text_input(
    "スペース区切りで入力してください （ex: 1m 2m 3m 1p...）",
    value=default_hand_str,
    help="m=萬子, p=筒子, s=索子, z=字牌"
)

#入力されて文字列をリストに変換
hand_14=[t.strip() for t in hand_input.split() if t.strip()]

#バリエーションチェック
if len(hand_14) !=14:
    st.warning(f"⚠️ 現在 **{len(hand_14)}枚** 入力されています。正確に **14枚**入力してください。")
else:
    st.success(f"手牌チェックOK（14枚）:{' '.join(hand_14)}")

    if st.button("計算を実行する", type="primary"):
        with st.spinner("計算中..."):
            current_shanten, sorted_results=evaluate_nanikiru(hand_14)

            #シャンテン数の表示名変換
            shanten_names={-1: "和了（アガリ）", 0: "テンパイ", 1: "1シャンテン", 2:"2シャンテン", 3:"3シャンテン"}
            shanten_text=shanten_names.get(current_shanten, f"{current_shanten}シャンテン")

            st.metric(label="現在のシャンテン数", value=shanten_text)
            st.markdown("---")
            st.subheader("📊 打牌ごとの受け入れ枚数ランキング")

            for rank, (discard, data) in enumerate(sorted_results, 1):
                #1位をハイライト表示
                if rank==1:
                    st.markdown(f"### 🏆 **第1位:打[{discard}]** （受け入れ総枚数: **{data['total_ukeire']}枚**）")
                else:
                    st.markdown(f"**第{rank}位: 打 [{discard}]** （受け入れ総枚数: {data['total_ukeire']}枚）")

                #有効牌の内訳を綺麗に並べる
                if data["effective_tiles"]:
                    #修正点：t（牌の名前）が表示されるように修正
                    eff_list_str="、".join([f"{t}（残り{c}枚）"for t, c in data["effective_tiles"]])
                    st.write(f"有効牌: {eff_list_str}")
                else:
                    st.write("有効牌: なし")

                st.markdown("")