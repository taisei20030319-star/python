import time
import streamlit as st

st.title("pomodoro timer")
st.write("Pythonだけで作ったオリジナルのwebタイマー")

max_sets = st.number_input("繰り返すセット数", min_value = 1, max_value = 10, value = 3)
work_seconds = st.number_input("作業時間（秒）", min_value = 1, max_value = 300, value = 5)
break_seconds = st.number_input("休憩時間（秒）",min_value = 1, max_value = 300, value = 3)

if st.button("タイマースタート"):
    status_text = st.empty()
    progress_bar = st.progress(0)

    current_set = 1

    while current_set <= max_sets:
        status_text.subheader(f"{current_set} / {max_sets} セット：作業タイム")
        for i in range(work_seconds, 0, -1):
            st.metric(label = "作業残り時間", value = f"{i} 秒")
            time.sleep(1)

        st.success("作業終了、お疲れ様でした")

        status_text.subheader(f"{current_set} / {max_sets} セット：休憩タイム")
        for i in range(break_seconds, 0, -1):
            st.metric(label = "休憩残り時間", value = f"{i} 秒")
            time.sleep(1)

        st.info(f"{current_set} セット終了")
        current_set = current_set + 1

    status_text.subheader("全セット終了、お疲れ様でした")
    st.balloons()
