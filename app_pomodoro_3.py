import time
import streamlit as st
st.set_page_config(page_title = "pomodoro timer", page_icon = "🕰️", layout="centered")

st.title("🕰️ カスタム・ポモドーロタイマー")
st.write("集中と休憩をスマートに管理するWeb App")

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ 設定")
    max_sets = st.number_input("繰り返すセット数", min_value = 1, max_value = 10, value = 3)
    work_minutes = st.number_input("作業時間（分）", min_value = 1, max_value = 60, value = 25)
    break_minutes = st.number_input("休憩時間（分）", min_value = 1, max_value = 30, value = 5)

with col2:
    st.subheader("💡 ステータス")
    st.info("左側の設定を決めて、下のボタンを押す")

    work_seconds = work_minutes * 60
    break_seconds = break_minutes * 60

    if st.button("🚀 タイマーをスタート", use_container_width = True):
        current_set = 1

        timer_display = st.empty()

        while current_set <= max_sets:

            timer_display.markdown(f"### 🔥 {current_set}セット：作業中")
            for i in range(work_seconds, 0, -1):
                mins = i // 60
                secs = i % 60
                st.metric(label = "残り作業時間", value = f"{mins}分 {secs}秒")
                time.sleep(1)

            st.success(f"{current_set}セットの作業終了、お疲れ様でした")

            timer_display.markdown(f"### ☕️ {current_set} セット：休憩中")
            for i in range(break_seconds, 0, -1):
                mins = i // 60
                secs = i % 60
                st.metric(label = "残り休憩時間", value = f"{mins}分 {secs}秒")
                time.sleep(1)

            st.info(f"{current_set}セット終了")
            current_set = current_set + 1

        timer_display.markdown("### 🎉 全セット終了、お疲れ様でした")
        st.balloons()
        