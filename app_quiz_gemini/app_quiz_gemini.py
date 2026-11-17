
import streamlit as st
import json
from google import genai

# =====================================
# ページ設定
# =====================================

st.set_page_config(
    page_title="AIクイズ",
    page_icon="🌏",
    layout="centered"
)

st.title("🌏 AIクイズ")
st.write("Geminiがクイズを作成します！")

# =====================================
# API設定
# =====================================

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=API_KEY)

except Exception as e:
    st.error(f"APIキーの読み込みエラー: {e}")
    st.stop()


# =====================================
# ジャンル選択
# =====================================

genre = st.selectbox(
    "📚 クイズのジャンル",
    [
        "一般常識",
        "世界遺産",
        "日本の地理・都道府県",
        "日本の観光名所・観光地",
        "世界の観光地・旅行",
        "日本の温泉・絶景スポット",
        "日本の郷土料理・名物",
        "世界の文化・伝統",
        "歴史・地理",
        "麻雀のルール・戦術",
        "Pythonプログラミング",
        "アニメ・映画・サブカル"
    ]
)

# =====================================
# 難易度選択
# =====================================

difficulty = st.select_slider(
    "⭐ 難易度を選択",
    options=["初級", "中級", "上級"],
    value="中級"
)

# =====================================
# セッション状態
# =====================================

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "selected_choice" not in st.session_state:
    st.session_state.selected_choice = None

if "is_answered" not in st.session_state:
    st.session_state.is_answered = False

if "quiz_genre" not in st.session_state:
    st.session_state.quiz_genre = None

if "quiz_difficulty" not in st.session_state:
    st.session_state.quiz_difficulty = None


# =====================================
# クイズ生成関数
# =====================================

def generate_new_quiz(selected_genre, selected_difficulty):

    prompt = f"""
あなたはクイズ作成の専門家です。

ジャンル：{selected_genre}
難易度：{selected_difficulty}

上記のジャンルと難易度に合った
日本語の4択クイズを1問作成してください。

【必ず守るルール】

1. 問題は必ず1問だけ
2. 選択肢は必ず4つ
3. 選択肢はすべて文字列にする
4. 選択肢はすべて異なる内容にする
5. 正解は必ず1つだけ
6. 正解は選択肢の文字列と完全一致させる
7. 解説は分かりやすく詳しく書く
8. 実際の事実に基づいた問題にする
9. 問題や選択肢に曖昧な表現を使わない

【JSON形式】

必ず以下の形式だけで出力してください。

{{
    "question": "問題文",
    "choices": [
        "選択肢1",
        "選択肢2",
        "選択肢3",
        "選択肢4"
    ],
    "answer": "正解の選択肢",
    "explanation": "詳しい解説と豆知識"
}}

JSON以外の文章は出力しないでください。
"""

    # 最大3回まで生成を試す
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            if not response.text:
                raise ValueError("AIから回答がありません")

            quiz = json.loads(response.text)

            # データ形式の確認
            if not isinstance(quiz, dict):
                raise ValueError("JSON形式が正しくありません")

            question = quiz.get("question")
            choices = quiz.get("choices")
            answer = quiz.get("answer")
            explanation = quiz.get("explanation")

            # 問題文の確認
            if not isinstance(question, str) or not question.strip():
                raise ValueError("問題文がありません")

            # 選択肢の確認
            if not isinstance(choices, list) or len(choices) != 4:
                raise ValueError("選択肢が4つではありません")

            if not all(
                isinstance(choice, str) and choice.strip()
                for choice in choices
            ):
                raise ValueError("選択肢の形式が正しくありません")

            if len(set(choices)) != 4:
                raise ValueError("選択肢が重複しています")

            # 正解の確認
            if not isinstance(answer, str) or answer not in choices:
                raise ValueError("正解が選択肢に含まれていません")

            # 解説の確認
            if not isinstance(explanation, str) or not explanation.strip():
                raise ValueError("解説がありません")

            return {
                "question": question,
                "choices": choices,
                "answer": answer,
                "explanation": explanation
            }

        except Exception as e:

            if attempt == 2:
                st.error(f"クイズの生成に失敗しました: {e}")
                return None

            st.warning(
                f"問題を再生成しています... ({attempt + 1}/2)"
            )

    return None


# =====================================
# 新しいクイズを出題
# =====================================

if st.button("✨ 新しいクイズを出題する", type="primary"):

    with st.spinner("🤖 Geminiが問題を作成中..."):

        quiz = generate_new_quiz(genre, difficulty)

        if quiz is not None:

            st.session_state.quiz_data = quiz
            st.session_state.selected_choice = None
            st.session_state.is_answered = False
            st.session_state.quiz_genre = genre
            st.session_state.quiz_difficulty = difficulty

            st.rerun()


# =====================================
# クイズ表示
# =====================================

if st.session_state.quiz_data:

    quiz = st.session_state.quiz_data

    st.divider()

    st.caption(
        f"ジャンル：{st.session_state.quiz_genre} "
        f"｜ 難易度：{st.session_state.quiz_difficulty}"
    )

    st.subheader(f"❓ Q. {quiz['question']}")

    # 回答前
    if not st.session_state.is_answered:

        selected = st.radio(
            "答えを選んでください！",
            quiz["choices"],
            key="user_choice"
        )

        if st.button("回答する", type="primary"):

            st.session_state.selected_choice = selected
            st.session_state.is_answered = True

            st.rerun()

    # 回答後
    else:

        if st.session_state.selected_choice == quiz["answer"]:

            st.success("🎉 正解です！おめでとうございます！")

        else:

            st.error("❌ 残念！不正解です！")

            st.write(
                f"正解は **{quiz['answer']}** です。"
            )

        st.info(
            f"💡 **解説・豆知識**\n\n{quiz['explanation']}"
        )

        st.divider()

        if st.button("➡️ 次の問題へ", type="primary"):

            with st.spinner("新しい問題を作成中..."):

                new_quiz = generate_new_quiz(
                    st.session_state.quiz_genre,
                    st.session_state.quiz_difficulty
                )

                if new_quiz is not None:

                    st.session_state.quiz_data = new_quiz
                    st.session_state.selected_choice = None
                    st.session_state.is_answered = False

                    st.rerun()
